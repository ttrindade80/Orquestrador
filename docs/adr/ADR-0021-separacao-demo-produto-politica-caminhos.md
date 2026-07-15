---
name: ADR-0021-separacao-demo-produto-politica-caminhos
description: Separa motor compartilhado de telas, aplicacao demonstrativa, futuro produto real, raizes declarativas de telas e grupos funcionais de configuracao
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
    - docs/NOMENCLATURA.md
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_json_lancador.md
    - docs/contratos/contrato_json_barra_de_menus.md
    - docs/contratos/contrato_json_cabecalho.md
    - docs/contratos/contrato_cabecalho.md
    - docs/contratos/contrato_estilo.md
  handoffs_bloqueados: []
---

# ADR-0021 — Separacao entre demonstracao, produto real e politica de caminhos

## Status

aceita

## Data

2026-07-14

---

## Contexto

O ultimo ciclo fechado e o H-0031.

Estado comprovado antes do levantamento:

- branch `master`;
- HEAD abreviado `0143fd1`;
- raiz operacional e Git unicas;
- estrutura existente com `config/`, `docs/` e `tela/`;
- `demo/` ainda nao existe;
- `config/telas/demo/` ainda nao existe;
- `orquestrador.py` ainda nao existe;
- suite canonica anterior composta por seis scripts executados diretamente da
  raiz;
- resultado anterior documentado: `1796/1796`.

O levantamento atual foi registrado em:

```text
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
```

Esse levantamento confirmou que:

- `tela/loader.py`, `tela/modelo.py` e `tela/renderizador.py` possuem funcao
  generica e reutilizavel;
- `tela/demo.py`, `tela/diagnostico.py` e
  `tela/explorar_barra_de_menus.py` possuem funcao demonstrativa ou
  exploratoria;
- os imports e testes atuais dependem do pacote `tela`;
- o loader atual usa diretamente `config/telas/<id>.json`;
- o nome do arquivo e o campo `id` devem coincidir;
- a ADR-0009 define atualmente `config/telas/<id>.json`;
- `config/estilo.json` possui autoridade documental propria e permanece fora
  de `config/telas/`;
- a criacao do futuro `orquestrador.py` e da tela real minima ainda pertence a
  decisao documental separada.

---

## Decisoes

As decisoes abaixo registram somente decisoes ja tomadas pelo usuario. Esta ADR
nao implementa migracao, nao define assinaturas, nao escolhe mecanismo concreto
de injecao de caminho, nao cria schema novo e nao aplica alteracoes aos demais
documentos.

### D1 — Motor compartilhado de telas

O diretorio:

```text
tela/
```

permanece na raiz como motor compartilhado de telas.

Devem permanecer conceitualmente nesse motor:

```text
tela/__init__.py
tela/loader.py
tela/modelo.py
tela/renderizador.py
```

Os testes especificos desses componentes genericos tambem permanecem associados
ao motor compartilhado:

```text
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

O motor compartilhado sera reutilizado tanto pela demonstracao quanto pelo
futuro `orquestrador.py`.

E proibida a criacao de uma segunda implementacao equivalente do loader, modelo
ou renderizador apenas para o produto real.

### D2 — Aplicacao demonstrativa

Sera criado o diretorio estrutural:

```text
demo/
```

Ele contera os pontos de entrada, utilitarios e testes que forem exclusivos da
demonstracao.

A migracao futura devera abranger conceitualmente:

```text
tela/demo.py
tela/diagnostico.py
tela/explorar_barra_de_menus.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
```

Esta ADR nao define assinatura de funcoes, imports concretos nem necessidade de
`demo/__init__.py`.

Esses detalhes poderao ser tratados no handoff e na implementacao, desde que:

- nao dupliquem o motor compartilhado;
- nao recriem compatibilidade com os caminhos antigos;
- preservem a execucao reproduzivel dos testes e demonstracoes.

### D3 — Telas declarativas da demonstracao

Sera criado o diretorio:

```text
config/telas/demo/
```

Todas as telas declarativas atualmente existentes diretamente em:

```text
config/telas/
```

serao tratadas como telas da demonstracao e migradas para esse novo diretorio
no ciclo de implementacao correspondente.

Isso inclui:

```text
config/telas/destino_minimo.json
config/telas/grupo_minimo.json
config/telas/h0029_dashboard_fracao.json
config/telas/h0029_dashboard_igual.json
config/telas/h0029_dashboard_percentual.json
config/telas/h0029_grupo_fracao.json
config/telas/h0029_grupo_igual.json
config/telas/h0029_grupo_pai_distribuido.json
config/telas/h0029_grupo_percentual.json
config/telas/h0030_console_unico.json
config/telas/h0030_dashboard_unico.json
config/telas/h0030_matriz_2x2.json
config/telas/h0030_matriz_2x4.json
config/telas/h0030_matriz_3x2.json
config/telas/stub_b.json
```

Os IDs internos dessas telas permanecem inalterados, salvo decisao documental
posterior especifica.

### D4 — Identidade da demonstracao

A atual tela:

```text
config/telas/orquestrador.json
```

deixara de representar o Orquestrador real e passara a representar
exclusivamente a demonstracao.

Na futura implementacao, ela sera migrada para:

```text
config/telas/demo/demo.json
```

Seu identificador interno sera:

```json
"id": "demo"
```

O ponto de entrada demonstrativo devera iniciar pela identidade `demo`, e nao
mais pela identidade `orquestrador`.

Nao sera criado alias entre `demo` e `orquestrador`.

### D5 — Telas do Orquestrador real

O diretorio:

```text
config/telas/
```

permanece como raiz das telas declarativas do Orquestrador real.

Depois da migracao das telas atuais para `config/telas/demo/`, os arquivos
diretamente em `config/telas/` serao reservados ao produto real.

A futura tela real:

```text
config/telas/orquestrador.json
```

nao faz parte desta ADR estrutural como conteudo ou implementacao.

Sua composicao, campos, barra de menus e relacao com `orquestrador.py` serao
definidos em ADR separada.

### D6 — Politica de resolucao das telas

A demonstracao e o produto real usarao o mesmo motor compartilhado, mas terao
raizes declarativas distintas:

```text
demonstracao: config/telas/demo/
produto real: config/telas/
```

A futura implementacao devera permitir que cada ponto de entrada utilize
explicitamente a raiz declarativa correspondente.

Esta ADR nao prescreve:

- assinatura de funcao;
- parametro especifico;
- classe;
- variavel;
- mecanismo concreto de injecao do caminho.

Fica estabelecido que:

- nao havera busca ambigua entre as duas raizes;
- nao havera fallback silencioso de uma raiz para a outra;
- nao havera duplicacao do mesmo JSON nas duas raizes;
- uma tela da demonstracao nao sera tratada como tela real apenas por
  coincidencia de ID.

### D7 — Ausencia de compatibilidade transitoria

A migracao futura sera direta.

Nao serao preservados:

- wrappers nos caminhos antigos;
- aliases do pacote `tela` para `demo`;
- copias duplicadas dos scripts;
- copias duplicadas dos JSON;
- fallback para `config/telas/<id>.json` quando o ponto de entrada estiver
  usando a raiz da demonstracao;
- alias entre os IDs `orquestrador` e `demo`.

Imports, subprocessos, comandos, testes e documentacao operacional diretamente
afetados deverao ser atualizados no mesmo ciclo de implementacao.

A ausencia de compatibilidade nao autoriza quebra da suite: o handoff devera
permitir nominalmente todas as atualizacoes necessarias.

### D8 — Organizacao dos JSON gerais de configuracao

Serao criados os diretorios:

```text
config/layouts/
config/elementos/
```

A organizacao decidida e:

```text
config/layouts/layout_console.json
config/layouts/layout_dado.json
config/layouts/layout_menu.json
```

e:

```text
config/elementos/cabecalho.json
config/elementos/barra_de_menus.json
config/elementos/lancador.json
```

Essa organizacao classifica os arquivos por funcao predominante.

A movimentacao nao altera, por si so:

- schema;
- conteudo;
- semantica;
- estado ativo, transicional ou obsoleto;
- autoridade documental de cada arquivo.

Arquivos transicionais continuam transicionais mesmo apos a mudanca de
diretorio.

### D9 — Preservacao de `config/estilo.json`

O arquivo:

```text
config/estilo.json
```

permanece temporariamente em seu caminho atual.

Ele nao sera movido para:

```text
config/layouts/
config/elementos/
config/telas/
config/telas/demo/
```

A eventual criacao de `config/estilos/` ou outra reorganizacao do sistema de
estilos dependera da futura ADR e implementacao da tela de estilos.

### D10 — Reutilizacao entre demonstracao e produto

A demonstracao continuara sendo o ambiente para:

- testar capacidades declarativas;
- validar telas criadas por JSON;
- executar cenarios de regressao;
- visualizar recursos antes de sua adocao no produto real.

Uma tela que utilize somente capacidades ja implementadas podera ser criada
declarativamente por JSON, sem nova implementacao de codigo.

Quando uma tela declarativa for transferida conceitualmente da demonstracao
para o produto real, ela devera reutilizar o mesmo:

- loader;
- modelo;
- renderizador;
- contratos de tela;
- regras de composicao ja implementadas.

Nao sera permitido reescrever o motor apenas para atender ao `orquestrador.py`.

### D11 — Tamanho do futuro handoff

A intencao inicial e produzir um handoff de implementacao unico depois da
aprovacao e aplicacao das ADRs necessarias.

Entretanto, essa intencao fica condicionada a coesao e extensao.

Se a criacao do handoff demonstrar que a lista nominal de:

- arquivos movidos;
- arquivos novos;
- imports;
- testes;
- comandos;
- configuracoes;
- documentacao operacional;
- criterios de demonstracao;

ficou excessivamente extensa ou reuniu capacidades materialmente independentes,
o gerente devera dividir a implementacao em mais de um handoff.

Essa divisao nao modifica a decisao arquitetural desta ADR.

---

## Relacao com ADRs anteriores

### ADR-0008

Preserva o modelo de configuracao declarativa por tela.

### ADR-0009

Substitui parcialmente a politica anterior de caminho unico:

```text
config/telas/<id>.json
```

A nova politica passa a distinguir:

```text
config/telas/<id>.json
config/telas/demo/<id>.json
```

conforme a identidade do ponto de entrada.

Preserva a decisao de que `config/estilo.json` nao pertence a
`config/telas/`.

### ADR-0010, ADR-0012, ADR-0014, ADR-0015, ADR-0018, ADR-0019 e ADR-0020

Preserva integralmente as regras funcionais de composicao, dashboard, barra de
menus, distribuicao e matriz.

A movimentacao estrutural nao altera essas semanticas.

### H-0031

Registra que o H-0031 estabeleceu a raiz independente atual com `config/`,
`docs/` e `tela/`.

Esta ADR nao reverte a raiz independente; ela apenas refina a separacao interna
entre motor compartilhado, demonstracao e produto real.

---

## Consequencias

- Criacao futura de `demo/`.
- Criacao futura de `config/telas/demo/`.
- Permanencia do motor compartilhado em `tela/`.
- Atualizacao futura dos imports e subprocessos demonstrativos.
- Mudanca do ID inicial da demonstracao para `demo`.
- Reserva de `config/telas/` para o produto real.
- Criacao futura de `config/layouts/` e `config/elementos/`.
- Atualizacao futura das autoridades que ainda fixam os caminhos antigos.
- Necessidade de preservar a suite canonica durante a migracao.
- Necessidade de atualizar comandos documentados.
- Inexistencia de compatibilidade transitoria.
- Proibicao de duplicacao do motor.

---

## Documentos potencialmente afetados

Esta ADR identifica documentos potencialmente afetados para futura aplicacao.
Nenhum deles e alterado nesta etapa.

Documentos minimos explicitamente afetados:

```text
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
```

Outros contratos com referencias reais a caminhos, identidades de tela,
elementos ou configuracoes que podem exigir atualizacao futura:

```text
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_estilo.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
```

Documentos operacionais e de indice com referencias reais a caminhos atuais ou
comandos atuais:

```text
docs/INDICE.md
docs/handoff/H-0030-catalogo-telas-utilizaveis.md
docs/handoff/H-0031-migracao-repositorio-orquestrador-raiz-independente.md
docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md
docs/relatorios/RELATORIO_QA_H-0031_IMPLEMENTACAO.md
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
```

Outros handoffs e relatorios historicos tambem contem referencias a
`config/telas/`, `tela/demo.py`, `tela/diagnostico.py`,
`tela/explorar_barra_de_menus.py`, `config/estilo.json` e arquivos gerais em
`config/`. A classificacao entre documento historico preservado e documento
operacional a atualizar devera ser feita no ciclo de aplicacao desta ADR.

---

## Fora do escopo

Esta ADR nao decide nem implementa:

- criacao de `orquestrador.py`;
- responsabilidade operacional de `orquestrador.py`;
- conteudo da futura tela real `config/telas/orquestrador.json`;
- composicao minima do Orquestrador real;
- remocao dos dados especificos do dashboard da tela atual;
- inclusao de `Esc`, `?` ou estilos na barra real;
- navegacao para a futura tela de estilos;
- implementacao da tela de estilos;
- alteracao de bordas ou envelopes de chips;
- integracao concreta com o Pipeline;
- mudanca de `config/estilo.json`;
- criacao de schema novo;
- alteracao da semantica dos elementos;
- correcao do preenchimento de `destino_minimo`;
- correcao do preenchimento de `grupo_minimo`;
- escolha da solucao para o problema de altura dos grupos;
- implementacao, testes ou movimentacao fisica de arquivos.

---

## Pendencias funcionais conhecidas

As pendencias abaixo ficam registradas separadamente e nao sao resolvidas por
esta ADR.

### `destino_minimo`

Comportamento desejado:

```text
preencher toda a area disponivel do corpo
```

Ha indicio de que uma alteracao declarativa usando distribuicao `igual` ou
`fracao` com peso unitario pode resolver o caso, mas:

```yaml
causa: NAO_CONFIRMADA
configuracao_exata: NAO_CONFIRMADA
solucao: NAO_CONFIRMADA
```

### `grupo_minimo`

Comportamento desejado:

```text
preencher toda a area disponivel do corpo
```

As tentativas manuais relatadas pelo usuario nao resolveram o caso.

```yaml
causa: NAO_CONFIRMADA
natureza_do_defeito: NAO_CONFIRMADA
solucao: NAO_CONFIRMADA
```

Esses itens exigirao levantamento focal reproduzivel e nao podem ser resolvidos
por suposicao nesta ADR.
