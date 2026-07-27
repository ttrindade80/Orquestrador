---
name: relatorio-levantamento-navegacao-selecao-unica-acoes
description: Levantamento documental e arquitetural sobre navegacao no console, selecao unica, Enter, acoes, retorno entre telas, paginacao, modos e fronteira Bloco 2/Bloco 3
metadata:
  type: relatorio
  etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
  escopo: Bloco_2_navegacao_selecao_unica_e_acoes
  status: concluido
---

# Relatorio de levantamento - navegacao, selecao unica e acoes

## 1. Identificacao

```yaml
etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
papel: pesquisador_documental_do_projeto_Orquestrador
atividade_priorizada: Bloco_2_navegacao_selecao_unica_e_acoes
branch_informada: master
HEAD_informado: bab30c5
arquivo_criado: docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
```

Este relatorio materializa em arquivo permanente o levantamento documental ja
realizado sobre navegacao no console, cursor, foco, selecao unica, Enter, acoes
declarativas, abertura e retorno entre telas, paginacao, modos verboso/nao
verboso e fronteira entre Bloco 2 e Bloco 3.

## 2. Objetivo

Registrar fatos documentais ja encontrados antes de chamar o usuario a decidir
qualquer dimensao nova do Bloco 2.

O objetivo deste arquivo e preservar:

- decisoes ja vigentes;
- decisoes parciais;
- decisoes explicitamente deferidas;
- exclusoes de ciclos anteriores;
- divergencias terminologicas;
- referencias nao encontradas ou nao confirmadas.

## 3. Escopo positivo

O levantamento cobre:

- navegacao interativa no `console`;
- cursor e posicao corrente;
- item em foco;
- selecao unica;
- tecla Enter;
- acao associada ao item;
- registro declarativo de acoes;
- abertura de outra tela;
- carregamento de conteudo multinivel da tela de destino;
- retorno a tela anterior;
- interacao com paginacao;
- interacao com modos verboso e nao verboso;
- fronteira documental entre Bloco 2 e Bloco 3.

## 4. Escopo negativo

Este relatorio nao:

- toma decisoes;
- propoe solucao;
- cria ADR, contrato, nomenclatura ou handoff;
- altera codigo ou configuracao;
- faz QA da propria documentacao;
- inicia implementacao;
- prepara stage, commit ou push;
- promove historico de implementacao a autoridade normativa final.

## 5. Estado Git inicial

Comandos registrados antes da criacao deste relatorio:

```bash
git status --short --untracked-files=all
git diff --name-status
git diff --cached --name-status
```

Saidas observadas:

```text
git status --short --untracked-files=all:

git diff --name-status:

git diff --cached --name-status:
```

Registro:

```yaml
workspace_inicial: LIMPO
stage_inicial: VAZIO
HEAD: bab30c5
```

## 6. Metodo de leitura seletiva

Foi preservado o metodo de leitura seletiva exigido pela documentacao vigente:

- uso de `docs/INDICE.md` e `docs/adr/INDICE_ADR.md` como roteadores;
- leitura do modulo proprietario do dominio de console;
- leitura dos contratos diretamente afetados;
- leitura de ADRs ja referenciadas pelos contratos e pelo levantamento anterior;
- leitura de handoffs e relatorios historicos apenas quando materialmente
  relevantes ao fluxo entre telas;
- conferencias focais posteriores somente para estado Git, existencia de arquivo
  e localizacao de `DOC-B009`.

Nao foi feita nova pesquisa ampla para produzir este relatorio.

## 7. Arquivos consultados

Arquivos efetivamente consultados no levantamento material anterior ou nas
conferencias focais deste registro:

```text
docs/INDICE.md
docs/adr/INDICE_ADR.md
docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
docs/nomenclatura/32_CONSOLE.md
docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_lancador.md
docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/handoff/H-0039-carregamento-global-materializacao-estilo.md
docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
docs/relatorios/RELATORIO_VALIDACAO_H-0010A_DECLARATIVA_STUB_B.md
docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md
```

Quantidade registrada: 25 arquivos.

## 8. Mapa de autoridades

| Documento | Papel no levantamento | Vigencia material |
|---|---|---|
| `docs/nomenclatura/32_CONSOLE.md` | Terminologia de console, cursor, selecao, item, `[✥]`, `ec`, `tg`, `tx` | Vigente |
| `docs/contratos/contrato_console.md` | Comportamento normativo do console | Ativo |
| `docs/contratos/contrato_barra_de_menus.md` | Chips, `[Esc]`, `[✥]`, `[␣]`, `[⏎]`, `[V]`, foco entre elementos | Ativo |
| `docs/contratos/contrato_tela_json.md` | JSON estrutural, acoes declarativas, pipeline conceitual, fronteira com conteudo externo | Ativo |
| `docs/contratos/contrato_json_console.md` | Envelope do console e documento externo de conteudo | Ativo |
| `docs/contratos/contrato_chip.md` | Classe chip, existencia/ativo, relacao com estilo, pendencia DOC-B009 | Ativo |
| `docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md` | Exclusao do `lancador` de `[✥]` | Aceita |
| `docs/adr/ADR-0026-...` | Separacao entre JSON estrutural e conteudo externo | Aceita e aplicada |
| `docs/adr/ADR-0027-...` | Carregamento separado e associacao pelo ponto de entrada | Aceita e aplicada |
| `docs/adr/ADR-0028-...` | Apresentacoes multinivel e modos verboso/nao verboso | Aceita e aplicada |
| `docs/adr/ADR-0030-...` | Estilo materializado e fronteira Bloco 2/Bloco 3 | Aceita; Bloco 1 implementado |
| `docs/handoff/H-0010A-...` | Historico de abertura/retorno por `lancador` | Historico de implementacao |
| `docs/relatorios/IMP-0010A-...` | Evidencia de implementacao historica de `tela_atual`, `pilha_telas` e `tela_destino` | Historico |

## 9. Terminologia encontrada

```yaml
console:
  fonte: docs/nomenclatura/32_CONSOLE.md
  sentido: container_interativo_e_navegavel

cursor_ou_selecionado:
  fonte: docs/nomenclatura/32_CONSOLE.md secao 4.2
  sentido: aponta_um_item
  indicador_documental: "→"

item_em_foco:
  fonte: docs/contratos/contrato_console.md secao 9; docs/contratos/contrato_barra_de_menus.md secao 10
  sentido: alvo_dinamico_do_Enter_e_do_estado_do_chip

selecao:
  fonte: docs/nomenclatura/32_CONSOLE.md secao 4.2
  sentido: conjunto_nomeado_de_elementos
  observacao: selecionado/cursor nao e sinonimo de selecao multipla

incluido:
  fonte: docs/nomenclatura/32_CONSOLE.md secao 4.4; ADR-0030 D7
  sentido: indicador visual de inclusao em selecao multipla

modo_normal:
  fonte: contrato_console.md secao 6
  relacao: termo coexistente com modo_nao_verboso em certos contextos

modo_nao_verboso:
  fonte: ADR-0028; docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  relacao: modo compacto; divergencia terminologica com modo_normal preservada
```

## 10. Decisoes vigentes

### D-01

```yaml
tema: natureza_navegavel_do_console
regra_ou_decisao: "`console` e container interativo e navegavel generico."
arquivo: docs/nomenclatura/32_CONSOLE.md
secao_ou_referencia: secao 4.1; linhas 55-57 no levantamento anterior
tipo_de_artefato: nomenclatura
autoridade: modulo proprietario do dominio console
vigencia: vigente
classificacao: DECIDIDO_E_VIGENTE
observacoes: Nao e tela, lancador, dashboard ou barra_de_menus.
```

### D-02

```yaml
tema: entidade_navegada
regra_ou_decisao: "O cursor navega por itens, nao por linhas fisicas."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 7; tambem contrato_tela_json.md secao 12
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: Um item pode ocupar uma ou mais linhas fisicas.
```

### D-03

```yaml
tema: estrutura_do_item
regra_ou_decisao: "Todo item navegavel do console tem `ec`, `tg` e `tx`, nessa ordem."
arquivo: docs/nomenclatura/32_CONSOLE.md
secao_ou_referencia: secao 4.4
tipo_de_artefato: nomenclatura
autoridade: modulo console
vigencia: vigente
classificacao: DECIDIDO_E_VIGENTE
observacoes: A diferenca entre item com selecao real e item navegavel sem selecao esta no conteudo visual de `tg`, nao na estrutura.
```

### D-04

```yaml
tema: ec_cursor_selecao_unica
regra_ou_decisao: "`ec` e o espaco do cursor, onde aparece `selecionado` quando o cursor esta na linha."
arquivo: docs/nomenclatura/32_CONSOLE.md
secao_ou_referencia: secao 4.4
tipo_de_artefato: nomenclatura
autoridade: modulo console
vigencia: vigente
classificacao: DECIDIDO_E_VIGENTE
observacoes: Para selecao unica, contrato_console.md secao 8 define que o cursor e o alvo implicito de Enter.
```

### D-05

```yaml
tema: tg_inclusao_selecao_multipla
regra_ou_decisao: "`tg` e o espaco de toggle, onde aparece `incluido`."
arquivo: docs/nomenclatura/32_CONSOLE.md
secao_ou_referencia: secao 4.4
tipo_de_artefato: nomenclatura
autoridade: modulo console
vigencia: vigente
classificacao: DECIDIDO_E_VIGENTE
observacoes: O uso comportamental do toggle por espaco pertence a selecao multipla, Bloco 3.
```

### D-06

```yaml
tema: chip_navegar
regra_ou_decisao: "`[✥]` representa navegacao por setas dentro de console navegavel."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 7
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: A notacao documental `[✥]` e dica visual; o movimento e pelas setas fisicas.
```

### D-07

```yaml
tema: exclusao_lancador_dashboard_de_navegacao_por_cursor
regra_ou_decisao: "`[✥]` nao navega `lancador` nem `dashboard`."
arquivo: docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
secao_ou_referencia: decisao itens 1-3; contrato_console.md secao 7
tipo_de_artefato: ADR e contrato
autoridade: ADR-0005; contrato_console.md
vigencia: aceita e ativa
classificacao: DECIDIDO_E_VIGENTE
observacoes: O `lancador` abre telas por itens proprios via `tela_destino`, nao por cursor `[✥]`.
```

### D-08

```yaml
tema: foco_entre_elementos
regra_ou_decisao: "`[⇆]` alterna foco entre elementos de corpo quando ha multiplos elementos."
arquivo: docs/contratos/contrato_barra_de_menus.md
secao_ou_referencia: secao 8.3 e secao 20
tipo_de_artefato: contrato
autoridade: contrato_barra_de_menus.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: Nao e o mesmo que `[✥]`; `[⇆]` atua no nivel da tela.
```

### D-09

```yaml
tema: navegacao_dentro_do_elemento_em_foco
regra_ou_decisao: "`[✥]` navega dentro do elemento de corpo em foco quando esse elemento e um console navegavel."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 7; secao 15
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: Se outro elemento estiver em foco, `[✥]` pode existir mas ficar inativo conforme regra da barra.
```

### D-10

```yaml
tema: politica_selecao_unica
regra_ou_decisao: "`politica_selecao = \"unica\"` usa o cursor como item alvo; nao ha toggle."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 8
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: O item em foco e o alvo implicito de `[⏎]`.
```

### D-11

```yaml
tema: ausencia_chip_espaco_na_selecao_unica
regra_ou_decisao: "`[␣]` nao existe em instancias com selecao unica."
arquivo: docs/contratos/contrato_barra_de_menus.md
secao_ou_referencia: secao 12; contrato_console.md secao 8
tipo_de_artefato: contrato
autoridade: contrato_barra_de_menus.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: `[␣]` e reservado a selecao multipla.
```

### D-12

```yaml
tema: item_em_foco_alvo_implicito_enter
regra_ou_decisao: "Na selecao unica, o item em foco e alvo implicito de `[⏎]`."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 8
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: A documentacao nao fecha neste ponto a regra de foco inicial.
```

### D-13

```yaml
tema: efeito_do_enter
regra_ou_decisao: "`[⏎]` executa a acao do item em foco."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 9
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: O estado do chip e recalculado a cada render.
```

### D-14

```yaml
tema: propriedade_da_acao
regra_ou_decisao: "A acao pertence ao item ou ao binding do item, nao a tela inteira."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 9; contrato_tela_json.md secao 16 e secao 21
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: Itens diferentes podem ter acoes diferentes.
```

### D-15

```yaml
tema: acao_declarativa
regra_ou_decisao: "A acao e declarativa."
arquivo: docs/contratos/contrato_tela_json.md
secao_ou_referencia: secao 20
tipo_de_artefato: contrato
autoridade: contrato_tela_json.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: `tela.json` e declarativo, nao procedural.
```

### D-16

```yaml
tema: registro_ou_lista_permitida
regra_ou_decisao: "Toda `acao_enter` deve pertencer ao registro de acoes conhecidas ou whitelist."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 9 e regra R-8
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: O registry completo e DOC-B009, ainda futuro.
```

### D-17

```yaml
tema: proibicao_comandos_arbitrarios
regra_ou_decisao: "Comando arbitrario e proibido."
arquivo: docs/contratos/contrato_tela_json.md
secao_ou_referencia: secao 20
tipo_de_artefato: contrato
autoridade: contrato_tela_json.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: O contrato da exemplo proibido como string procedural de comando.
```

### D-18

```yaml
tema: regras_de_Esc
regra_ou_decisao: "`[Esc]` limpa selecao ativa; sem selecao sai na raiz; sem selecao volta em tela interna."
arquivo: docs/contratos/contrato_barra_de_menus.md
secao_ou_referencia: secao 9
tipo_de_artefato: contrato
autoridade: contrato_barra_de_menus.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: A limpeza de selecao tem precedencia sobre navegacao.
```

### D-19

```yaml
tema: historico_tela_atual_pilha_telas_tela_destino
regra_ou_decisao: "H-0010A implementou historicamente `tela_atual`, `pilha_telas` e `tela_destino` para fluxo minimo do `lancador`."
arquivo: docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
secao_ou_referencia: secoes 'Como a navegacao minima funciona' e 'Escopo implementado'
tipo_de_artefato: relatorio de implementacao
autoridade: evidencia historica, nao contrato final de Enter no console
vigencia: historico
classificacao: PREVISTO_SEM_COMPORTAMENTO_COMPLETO
observacoes: Nao deve ser promovido automaticamente para Enter no console.
```

### D-20

```yaml
tema: separacao_json_estrutural_conteudo_runtime
regra_ou_decisao: "JSON estrutural da tela e conteudo externo de runtime sao documentos separados."
arquivo: docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_referencia: decisao; contrato_tela_json.md secao 31
tipo_de_artefato: ADR e contrato
autoridade: ADR-0026; contrato_tela_json.md
vigencia: aceita e aplicada
classificacao: DECIDIDO_E_VIGENTE
observacoes: Conteudo do console nao volta a ser armazenado no JSON estrutural.
```

### D-21

```yaml
tema: carregamento_conjunto_ponto_entrada
regra_ou_decisao: "O ponto de entrada carrega separadamente JSON estrutural e documento externo quando aplicavel."
arquivo: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
secao_ou_referencia: D2, D3, D8; contrato_tela_json.md secao 32
tipo_de_artefato: ADR e contrato
autoridade: ADR-0027
vigencia: aceita e aplicada
classificacao: DECIDIDO_E_VIGENTE
observacoes: A associacao ocorre externamente ao JSON estrutural.
```

### D-22

```yaml
tema: responsabilidade_renderizador
regra_ou_decisao: "Renderizador calcula geometria, truncamento, paginacao e posicoes finais."
arquivo: docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_referencia: decisao item 11; contrato_console.md secao 19.4
tipo_de_artefato: ADR e contrato
autoridade: ADR-0026
vigencia: aceita e aplicada
classificacao: DECIDIDO_E_VIGENTE
observacoes: Documento externo nao contem resultados fisicos calculados.
```

### D-23

```yaml
tema: paginacao_por_conteudo_que_nao_cabe
regra_ou_decisao: "Paginacao e consequencia automatica do conteudo renderizado que nao cabe na area disponivel."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 12
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: Filtros sao aplicados antes da paginacao.
```

### D-24

```yaml
tema: pagina_atual_estado_runtime
regra_ou_decisao: "Pagina atual e estado de runtime, nao pertence ao JSON como estado vivo."
arquivo: docs/contratos/contrato_console.md
secao_ou_referencia: secao 12
tipo_de_artefato: contrato
autoridade: contrato_console.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: Selecao persiste entre paginas conforme regra ja registrada.
```

### D-25

```yaml
tema: politicas_modo_por_tela
regra_ou_decisao: "Telas de console multinivel novas ou revisadas declaram politica de modo: `somente_verboso`, `somente_nao_verboso` ou `alternavel`."
arquivo: docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
secao_ou_referencia: D23; contrato_tela_json.md secao 33.6
tipo_de_artefato: ADR e contrato
autoridade: ADR-0028
vigencia: aceita e aplicada
classificacao: DECIDIDO_E_VIGENTE
observacoes: Telas legadas permanecem validas sem reinterpretacao automatica.
```

### D-26

```yaml
tema: chip_V
regra_ou_decisao: "`[V]` e tecla `V` aplicam-se apenas a telas alternaveis."
arquivo: docs/contratos/contrato_barra_de_menus.md
secao_ou_referencia: secao 22
tipo_de_artefato: contrato
autoridade: contrato_barra_de_menus.md
vigencia: ativo
classificacao: DECIDIDO_E_VIGENTE
observacoes: Telas de modo unico nao expõem `V` como acao aplicavel.
```

### D-27

```yaml
tema: indicador_selecionado
regra_ou_decisao: "`indicadores.selecionado.preset_default = \"Seta\"`; simbolo resultante `→`."
arquivo: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
secao_ou_referencia: D6
tipo_de_artefato: ADR
autoridade: ADR-0030
vigencia: aceita; Bloco 1 implementado por H-0039
classificacao: DECIDIDO_E_VIGENTE
observacoes: O simbolo nao deve ser repetido como constante operacional no renderer.
```

### D-28

```yaml
tema: indicador_incluido
regra_ou_decisao: "`indicadores.incluido.preset_default = \"Círculo\"`; valores `●` e `○`."
arquivo: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
secao_ou_referencia: D7
tipo_de_artefato: ADR
autoridade: ADR-0030
vigencia: aceita; Bloco 1 implementado por H-0039
classificacao: DECIDIDO_E_VIGENTE
observacoes: O consumo comportamental pertence ao mecanismo de selecao multipla, Bloco 3.
```

### D-29

```yaml
tema: blocos_2_3_nao_implementados_por_ADR0030_H0039
regra_ou_decisao: "ADR-0030/H-0039 concluiu Bloco 1; Bloco 2 e Bloco 3 permaneceram futuros."
arquivo: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
secao_ou_referencia: status atual e D13; docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md secao 9
tipo_de_artefato: ADR e relatorio de implementacao
autoridade: ADR-0030; evidencia H-0039
vigencia: vigente
classificacao: EXCLUIDO_DE_CICLO_ANTERIOR
observacoes: Navegacao/selecao nao foram implementadas no Bloco 1.
```

## 11. Decisoes parciais

```yaml
- tema: foco_inicial
  estado: COMPORTAMENTO_PARCIALMENTE_DEFINIDO
  fato: ha regra para foco entre elementos por `[⇆]` e para `[✥]` dentro do elemento em foco
  lacuna: regra inicial de qual elemento ou item recebe foco nao foi confirmada
  autoridade: contrato_barra_de_menus.md secao 8.3; contrato_console.md secao 7

- tema: wrap_e_celula_vazia
  estado: COMPORTAMENTO_PARCIALMENTE_DEFINIDO
  fato: nomenclatura registra wrap toroidal, toróide por celula vazia e cursor sem entrar em celula vazia
  lacuna: algoritmo detalhado de implementacao permanece futuro
  autoridade: docs/nomenclatura/32_CONSOLE.md secao 4.3; contrato_console.md secao 18

- tema: item_sem_acao
  estado: COMPORTAMENTO_PARCIALMENTE_DEFINIDO
  fato: item sem `acao_enter` valida torna `[⏎]` inativo
  lacuna: comportamento quando ha binding inconsistente ou invalido alem da invalidade contratual nao foi detalhado como fluxo de runtime
  autoridade: contrato_console.md secao 9; contrato_tela_json.md secao 16

- tema: paginacao_e_modos
  estado: COMPORTAMENTO_PARCIALMENTE_DEFINIDO
  fato: modo normal/verboso altera numero de linhas por item e, portanto, itens por pagina
  lacuna: preservacao de cursor ao mudar pagina ou modo nao foi completamente fechada para todos os casos
  autoridade: contrato_console.md secoes 6 e 12
```

## 12. Decisoes deferidas

```yaml
- tema: registry_completo_de_acoes
  estado: DEFERIDO_EXPLICITAMENTE
  autoridade: contrato_console.md secao 18; contrato_json_console.md secao 8; contrato_chip.md secao 19

- tema: contratos_especificos_tipos_internos_item
  estado: DEFERIDO_EXPLICITAMENTE
  autoridade: contrato_console.md secao 18; contrato_json_console.md secao 8

- tema: navegacao_multinivel_expansao_recolhimento_paginacao_interativa
  estado: DEFERIDO_EXPLICITAMENTE
  autoridade: ADR-0027 secao D12; ADR-0027 secao decisoes deferidas

- tema: vinculo_final_fonte_externa_pipeline
  estado: DEFERIDO_EXPLICITAMENTE
  autoridade: ADR-0026 secao 14; contrato_tela_json.md secao 31.3

- tema: protocolo_script_externo
  estado: DEFERIDO_EXPLICITAMENTE
  autoridade: ADR-0026 secao 14; ADR-0027 secao 9.3

- tema: comportamento_fonte_ausente_ou_invalida
  estado: DEFERIDO_EXPLICITAMENTE
  autoridade: ADR-0026 secao 14; contrato_json_console.md secao 11.8
```

## 13. Exclusoes de ciclos anteriores

```yaml
- ciclo: H-0010A
  exclusoes:
    - console_real
    - filtros
    - paginacao
    - selecao
    - toggle
    - modo_verboso
    - navegacao_por_[✥]
    - registry_completo_de_telas
    - registry_completo_de_acoes
  classificacao: EXCLUIDO_DE_CICLO_ANTERIOR
  autoridade: docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md secao Escopo negativo

- ciclo: H-0036
  exclusoes:
    - navegacao_multinivel
    - expansao_ou_recolhimento
    - paginacao_interativa
  classificacao: EXCLUIDO_DE_CICLO_ANTERIOR
  autoridade: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md D12

- ciclo: H-0039
  exclusoes:
    - Bloco_2
    - Bloco_3
  classificacao: EXCLUIDO_DE_CICLO_ANTERIOR
  autoridade: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md secao 9
```

## 14. Foco, selecao unica e acao

```yaml
foco:
  conceito: item_atual_ou_elemento_atual_relevante_para_estado_dinamico
  autoridade:
    - docs/contratos/contrato_console.md secao 7
    - docs/contratos/contrato_barra_de_menus.md secoes 10 e 11
  comportamento_decidido:
    - "[⇆] alterna foco entre elementos de corpo quando ha multiplos elementos"
    - "[✥] navega dentro do console em foco"
    - "[⏎] recalcula estado com base no item em foco"
  comportamento_aberto:
    - regra_inicial_do_foco
    - preservacao_do_foco_ao_mudar_pagina
    - preservacao_do_foco_ao_mudar_modo_em_todos_os_casos

selecao_unica:
  conceito: politica_em_que_o_cursor_define_o_item_alvo
  autoridade:
    - docs/contratos/contrato_console.md secao 8
    - docs/contratos/contrato_barra_de_menus.md secao 12
  relacao_com_foco: item_em_foco_e_alvo_implicito_de_Enter
  toggle: ausente; "[␣] nao existe"
  indicador: relacionado_ao_cursor_em_ec_por_indicador_selecionado
  comportamento_aberto:
    - inicializacao_do_cursor
    - persistencia_ou_restauracao_do_cursor_ao_retornar_de_tela

acao:
  entidade_proprietaria: item_ou_binding_do_item
  gatilho: "[⏎]"
  forma_declarativa: acao_enter_ou_acao_registrada_no_JSON
  restricoes:
    - deve_ser_registrada_ou_whitelisted
    - comando_arbitrario_proibido
    - item_sem_acao_valida_torna_Enter_inativo
  comportamento_aberto:
    - registry_completo_DOC_B009
    - parametros_formais_dos_tipos_de_acao
    - comportamento_detalhado_de_binding_invalido_em_runtime
```

Nao foi encontrada autoridade suficiente para declarar que foco e selecao unica
sao estados diferentes. Tambem nao foi encontrada autoridade suficiente para
declara-los equivalentes alem da regra: na selecao unica, o cursor define o item
alvo e o item em foco e alvo implicito de Enter.

## 15. Navegacao entre elementos e dentro do console

```yaml
entre_elementos:
  chip: "[⇆]"
  autoridade: contrato_barra_de_menus.md secao 8.3
  decisao: alterna foco entre elementos de corpo
  estado: DECIDIDO_E_VIGENTE

dentro_do_console:
  chip: "[✥]"
  autoridade: contrato_console.md secao 7
  decisao: setas movem o cursor por item navegavel dentro do console em foco
  estado: DECIDIDO_E_VIGENTE

exclusoes:
  lancador: nao_navegavel_por_[✥]
  dashboard: nao_navegavel_por_[✥]
  autoridade: ADR-0005; contrato_console.md; contrato_barra_de_menus.md
```

## 16. Abertura e retorno entre telas

### 16.1 Comportamento historicamente implementado no `lancador`

H-0010A implementou fluxo minimo de `lancador`:

```text
chip do lancador -> push tela_atual em pilha_telas; tela_atual = tela_destino
Esc com pilha_telas nao vazia -> pop; tela_atual = tela anterior
Esc com pilha_telas vazia -> sair
```

Autoridades historicas:

- `docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md`;
- `docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md`;
- `docs/relatorios/RELATORIO_VALIDACAO_H-0010A_DECLARATIVA_STUB_B.md`.

Classificacao: `PREVISTO_SEM_COMPORTAMENTO_COMPLETO`.

### 16.2 Comportamento ja contratado de `[Esc]`

`[Esc]` possui regra contextual vigente em `contrato_barra_de_menus.md` secao 9:

- com selecao ativa, limpa selecao;
- sem selecao ativa na raiz, sai;
- sem selecao ativa em outra tela, volta.

Classificacao: `DECIDIDO_E_VIGENTE`.

### 16.3 Comportamento futuro de Enter no item de `console`

O contrato ja define que `[⏎]` executa a acao do item em foco e que essa acao
e declarativa e registrada. Nao foi encontrada implementacao historica que
promova automaticamente o mecanismo de `lancador` para Enter do `console`.

Classificacao: `COMPORTAMENTO_PARCIALMENTE_DEFINIDO`.

### 16.4 Pontos ainda nao definidos

```yaml
pontos_abertos:
  - reutilizacao_ou_nao_de_tela_atual
  - reutilizacao_ou_nao_de_pilha_telas
  - mecanismo_equivalente_para_historico_de_telas
  - preservacao_do_estado_da_tela_de_origem
  - associacao_formal_entre_acao_enter_e_abertura_de_tela
```

## 17. Paginacao e modos verboso/nao verboso

```yaml
pagina_atual:
  decisao: estado_de_runtime
  autoridade: contrato_console.md secao 12

filtros:
  decisao: aplicados_antes_da_paginacao
  autoridade: contrato_console.md secao 11 e secao 12

linhas_por_item:
  decisao: modo_normal_ou_verboso_altera_numero_de_linhas_por_item
  efeito: altera_numero_de_itens_por_pagina
  autoridade: contrato_console.md secao 12

modo_nao_verboso:
  decisao: conteudo_aplicavel_ocupa_uma_linha_fisica
  autoridade: contrato_console.md secao 21.2; ADR-0028 D9

modo_verboso:
  decisao: conteudo_pode_ocupar_varias_linhas_fisicas
  autoridade: contrato_console.md secao 21.3; ADR-0028 D10

preservacao_cursor_ao_mudar_modo:
  fato: contrato_console.md secao 6 afirma que transicao entre modos nao altera cursor, selecao nem filtros ativos
  classificacao: DECIDIDO_E_VIGENTE
  limite: nao detalha todos os cenarios de pagina e impossibilidade geometrica

preservacao_selecao_ao_mudar_modo:
  fato: contrato_console.md secao 6 afirma que transicao entre modos nao altera selecao
  classificacao: DECIDIDO_E_VIGENTE
  limite: Bloco 3 permanece futuro para selecao multipla

mudanca_automatica_de_pagina_durante_navegacao:
  fato: docs/nomenclatura/32_CONSOLE.md secao 4.3 afirma que cursor nunca troca de pagina sozinho ao cruzar borda do toroide
  classificacao: DECIDIDO_E_VIGENTE
```

Nao foi derivada politica adicional de cursor apenas a partir da politica de
paginacao.

## 18. Indicadores visuais ja materializados

```yaml
selecionado:
  origem: config/estilo.json via ADR-0030 D6
  preset_default: "Seta"
  simbolo: "→"
  uso_documental: cursor/item_sob_cursor no espaco `ec`
  estado: DECIDIDO_E_VIGENTE
  observacao: H-0039 concluiu carregamento/materializacao de estilo; comportamento de navegacao continua futuro

incluido:
  origem: config/estilo.json via ADR-0030 D7
  preset_default: "Círculo"
  on: "●"
  off: "○"
  uso_documental: inclusao/toggle no espaco `tg`
  estado: DECIDIDO_E_VIGENTE
  observacao: consumo comportamental pertence ao Bloco 3
```

## 19. Analise de `DOC-B009`

### 19.1 Ocorrencias encontradas

Conferencia focal:

```text
docs/contratos/contrato_chip.md:497-500
docs/contratos/contrato_console.md:516-518
docs/contratos/contrato_json_console.md:231
```

### 19.2 Necessidade representada

`DOC-B009` representa o registry completo de acoes:

- tipos de `acao_enter` declaraveis;
- parametros das acoes;
- lista de tipos de acao reconhecidos pelo renderer;
- no contrato de chip, tambem aparece associado ao registry completo de tipos de chip.

### 19.3 Arquivo proprio correspondente

Conferencia focal por nome `*B009*` em `docs/` nao encontrou arquivo proprio.

```yaml
arquivo_proprio_DOC_B009: NAO_ENCONTRADO
classificacao_materialidade: NAO_CONFIRMADO
```

### 19.4 Natureza atual

```yaml
natureza: identificador_referenciado_sem_artefato_atual_confirmado
item_de_backlog: NAO_CONFIRMADO
referencia_historica: NAO_CONFIRMADO
identificador_sem_artefato_atual: CONFIRMADO_POR_AUSENCIA_DE_ARQUIVO_NOMEADO
```

### 19.5 Regras ja decididas independentemente de `DOC-B009`

```yaml
regras_ja_decididas:
  - acao_enter_pertence_ao_item_ou_binding
  - Enter_executa_acao_do_item_em_foco
  - item_sem_acao_valida_torna_Enter_inativo
  - acao_deve_ser_declarativa
  - acao_deve_ser_registrada_ou_whitelisted
  - comando_arbitrario_e_proibido
```

### 19.6 Partes ainda dependentes de definicao futura

```yaml
dependem_de_DOC_B009_ou_tarefa_futura:
  - catalogo_exaustivo_de_tipos_de_acao
  - parametros_formais_de_cada_tipo_de_acao
  - registry_completo_do_dispatcher
  - lista_exaustiva_de_tipos_de_chip_reconhecidos
```

Nao foi inventado conteudo para `DOC-B009`.

## 20. Fronteira entre Bloco 2 e Bloco 3

```yaml
Bloco_2:
  - navegacao_por_setas
  - cursor
  - foco
  - selecao_unica
  - Enter
  - acao_individual
  - abertura_de_tela_conhecida

Bloco_3:
  - selecao_multipla
  - toggle_por_espaco
  - conjunto_de_itens_incluidos
  - uso_de_incluido_on_e_incluido_off
  - acao_sobre_conjunto
```

Documentos que antecipam elementos de ambos os blocos:

- `docs/nomenclatura/32_CONSOLE.md`: distingue cursor/selecionado de selecao e
  define `ec`/`tg`;
- `docs/contratos/contrato_console.md`: define politicas `nenhuma`, `unica`,
  `multipla`, Enter por item e selecao como estado de runtime;
- `docs/contratos/contrato_barra_de_menus.md`: define `[✥]`, `[␣]`, `[⏎]` e
  `[Esc]`;
- `docs/adr/ADR-0030-...`: materializa indicadores de cursor e inclusao, mas
  exclui Blocos 2 e 3 do Bloco 1.

Os blocos nao foram unidos neste relatorio.

## 21. Matriz consolidada

| Dimensao | Decisao encontrada | Autoridade | Estado | Lacuna restante |
|---|---|---|---|---|
| natureza navegavel do console | Console e container interativo e navegavel | `32_CONSOLE.md`; `contrato_console.md` | DECIDIDO_E_VIGENTE | Implementacao concreta do cursor |
| entidade navegada | Cursor navega por item, nao linha fisica | `contrato_console.md` secao 7 | DECIDIDO_E_VIGENTE | Algoritmo detalhado |
| estrutura `ec`/`tg`/`tx` | Item tem tres partes fixas | `32_CONSOLE.md` secao 4.4 | DECIDIDO_E_VIGENTE | Renderizacao operacional no Bloco 2/3 |
| politica de selecao unica | Cursor define alvo; sem toggle | `contrato_console.md` secao 8 | DECIDIDO_E_VIGENTE | Estado inicial do cursor |
| cursor inicial | Nao confirmado | Nao encontrado | NAO_CONFIRMADO | DECISAO_AUSENTE |
| foco inicial | Nao confirmado | Nao encontrado | NAO_CONFIRMADO | DECISAO_AUSENTE |
| movimento horizontal | Previsto por setas e wrap toroidal | `32_CONSOLE.md`; `contrato_console.md` | COMPORTAMENTO_PARCIALMENTE_DEFINIDO | Detalhe de algoritmo |
| movimento vertical | Previsto por setas e wrap toroidal | `32_CONSOLE.md`; `contrato_console.md` | COMPORTAMENTO_PARCIALMENTE_DEFINIDO | Detalhe de algoritmo |
| celulas vazias | Cursor nunca entra em celula vazia | `32_CONSOLE.md` secao 4.3 | COMPORTAMENTO_PARCIALMENTE_DEFINIDO | Implementacao detalhada |
| linha incompleta | Nao confirmado como regra propria | Nao encontrado | NAO_CONFIRMADO | DECISAO_AUSENTE |
| limites da matriz | Wrap toroidal fecha bordas | `32_CONSOLE.md` secao 4.3 | COMPORTAMENTO_PARCIALMENTE_DEFINIDO | Regras detalhadas por layout |
| wrap | Wrap toroidal por eixo | `32_CONSOLE.md` secao 4.3 | DECIDIDO_E_VIGENTE | Implementacao futura |
| foco entre elementos | `[⇆]` alterna foco | `contrato_barra_de_menus.md` | DECIDIDO_E_VIGENTE | Foco inicial |
| navegacao dentro do elemento | `[✥]` navega console em foco | `contrato_console.md` | DECIDIDO_E_VIGENTE | Estado vivo |
| foco versus selecao | Cursor/foco aponta item; selecao e conjunto | `32_CONSOLE.md`; `contrato_console.md` | DECIDIDO_E_VIGENTE | Distincao estado-a-estado nao totalmente formalizada |
| indicador da selecao unica | `selecionado`/Seta/`→` para cursor | ADR-0030 D6 | DECIDIDO_E_VIGENTE | Consumo pelo comportamento de navegacao |
| chip `[✥]` | Navegacao por setas em console navegavel | `contrato_barra_de_menus.md`; `contrato_console.md` | DECIDIDO_E_VIGENTE | Implementacao Bloco 2 |
| chip `[⏎]` | Acao do item em foco | `contrato_barra_de_menus.md`; `contrato_console.md` | DECIDIDO_E_VIGENTE | Registry completo |
| chip `[␣]` | Apenas selecao multipla | `contrato_barra_de_menus.md` secao 12 | DECIDIDO_E_VIGENTE | Bloco 3 |
| ordem dos chips | Ordem canonica; declaracao deve respeitar | `contrato_barra_de_menus.md` secao 7; ADR-0030 D13 | DECIDIDO_E_VIGENTE | Validacao concreta |
| efeito do Enter | Executa acao do item em foco | `contrato_console.md` secao 9 | DECIDIDO_E_VIGENTE | Tipos concretos de acao |
| item sem acao | Enter inativo | `contrato_console.md`; `contrato_barra_de_menus.md` | DECIDIDO_E_VIGENTE | Binding invalido em runtime |
| acao declarativa | JSON declarativo, nao procedural | `contrato_tela_json.md` secao 20 | DECIDIDO_E_VIGENTE | Registry |
| registry de acoes | DOC-B009 futuro | `contrato_console.md`; `contrato_chip.md` | DECIDIDO_MAS_DEFERIDO | Arquivo proprio nao encontrado |
| lista permitida | Whitelist/registro exigidos | `contrato_console.md` | DECIDIDO_E_VIGENTE | Conteudo da lista |
| comandos arbitrarios | Proibidos | `contrato_tela_json.md` secao 20 | DECIDIDO_E_VIGENTE | Nenhuma neste levantamento |
| tela de destino | Historico no `lancador` via `tela_destino` | H-0010A; IMP-0010A | PREVISTO_SEM_COMPORTAMENTO_COMPLETO | Aplicacao a Enter do console |
| abertura de outra tela | Implementada historicamente no `lancador` | IMP-0010A | PREVISTO_SEM_COMPORTAMENTO_COMPLETO | Mecanismo final para console |
| retorno por Esc | Voltar em tela interna sem selecao | `contrato_barra_de_menus.md` secao 9 | DECIDIDO_E_VIGENTE | Integracao com acao Enter |
| pilha ou historico de telas | Historico `pilha_telas` no H-0010A | IMP-0010A | PREVISTO_SEM_COMPORTAMENTO_COMPLETO | Reuso nao decidido |
| preservacao do estado da origem | Nao confirmado | Nao encontrado | NAO_CONFIRMADO | DECISAO_AUSENTE |
| paginacao | Conteudo que nao cabe cria paginas | `contrato_console.md` secao 12 | DECIDIDO_E_VIGENTE | Algoritmo e interacao |
| mudanca automatica de pagina | Cursor nao troca pagina sozinho ao cruzar toroide | `32_CONSOLE.md` secao 4.3 | DECIDIDO_E_VIGENTE | Comandos especificos de pagina |
| modo verboso/nao verboso | Politica por tela D23 | ADR-0028; contrato_tela_json.md | DECIDIDO_E_VIGENTE | Divergencia terminologica |
| preservacao de foco ao mudar modo | Transicao nao altera cursor | `contrato_console.md` secao 6 | DECIDIDO_E_VIGENTE | Casos de pagina/impossibilidade |
| preservacao de selecao ao mudar modo | Transicao nao altera selecao | `contrato_console.md` secao 6 | DECIDIDO_E_VIGENTE | Bloco 3 futuro |
| redimensionamento | Recalcula tela e paginacao autorizada | `contrato_tela_json.md` secao 24 | DECIDIDO_E_VIGENTE | Interacao fina com cursor |
| conteudo externo da tela de destino | JSON externo separado; ponto de entrada carrega | ADR-0026; ADR-0027 | DECIDIDO_E_VIGENTE | Vinculo final/Pipeline |
| fronteira Bloco 2/Bloco 3 | Bloco 2 individual; Bloco 3 selecao multipla | ADR-0030 D13 | DECIDIDO_E_VIGENTE | Handoff futuro |

## 22. Contradicoes

```yaml
contradicoes_entre_autoridades_ativas: nenhuma_confirmada
observacao: nao foi feita QA; esta secao registra apenas contradicoes materiais encontradas no levantamento
```

## 23. Divergencias terminologicas

```yaml
- tema: modo_normal_vs_modo_nao_verboso
  classificacao: DIVERGENCIA_TERMINOLOGICA
  autoridade: docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md secao 4.4; contrato_console.md secao 21.4
  registro: os dois termos coexistem para o mesmo referente em contextos de apresentacao do console
  restricao: qualquer reconciliacao requer nova ADR
```

## 24. Referencias nao encontradas

```yaml
- referencia: arquivo_proprio_DOC_B009
  resultado: NAO_ENCONTRADO
  conferencia: find docs -name '*B009*' -print
  observacao: identificador aparece em contratos, mas arquivo proprio nao foi localizado

- referencia: regra_inicial_cursor
  resultado: NAO_ENCONTRADO
  observacao: nao foi encontrada regra material que defina o primeiro item sob cursor

- referencia: regra_inicial_foco
  resultado: NAO_ENCONTRADO
  observacao: nao foi encontrada regra material que defina o elemento inicialmente em foco

- referencia: preservacao_estado_origem_apos_abrir_destino_por_Enter
  resultado: NAO_ENCONTRADO
  observacao: historico do lancador nao decide Enter do console
```

## 25. Dimensoes abertas para decisao futura

```yaml
- implementacao_do_cursor
- posicao_corrente
- regra_inicial_do_foco
- movimento_horizontal
- movimento_vertical
- comportamento_detalhado_nos_limites
- wrap_detalhado
- tratamento_de_celula_vazia
- linha_incompleta
- registry_completo_de_acoes
- contratos_especificos_dos_tipos_internos_de_item
- acao_de_item_sem_binding_valido
- navegacao_multinivel
- expansao_e_recolhimento
- paginacao_interativa
- vinculo_final_com_fonte_externa_ou_Pipeline
- protocolo_do_script_externo
- comportamento_diante_de_fonte_ausente_ou_invalida
- preservacao_do_estado_da_tela_de_origem
- reuso_ou_nao_de_tela_atual_e_pilha_telas_para_Enter_do_console
```

Quantidade registrada: 20 dimensoes abertas.

## 26. Fatos `NAO_CONFIRMADOS`

```yaml
- arquivo_proprio_DOC_B009
- DOC_B009_como_item_de_backlog_material
- regra_inicial_do_cursor
- regra_inicial_do_foco
- equivalencia_formal_entre_foco_e_selecao_unica
- diferenca_formal_completa_entre_foco_e_selecao_unica_como_estados_distintos
- preservacao_do_estado_da_tela_de_origem
- aplicacao_automatica_do_mecanismo_do_lancador_ao_Enter_do_console
- regra_de_linha_incompleta_para_navegacao
```

## 27. Estado Git final

Comandos executados apos a criacao deste relatorio:

```bash
git status --short --untracked-files=all
git diff --name-status
git diff --check
git diff --cached --name-status
```

Saidas observadas:

```text
git status --short --untracked-files=all:
?? docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md

git diff --name-status:

git diff --check:

git diff --cached --name-status:
```

Registro:

```yaml
arquivo_criado:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
outros_arquivos_alterados: nenhum
stage: VAZIO
workspace_final: UM_ARQUIVO_NAO_RASTREADO
```

## 28. Conclusao

O levantamento confirma que ha base documental vigente suficiente para separar
cursor, item em foco, selecao unica, Enter declarativo, retorno por Esc,
paginacao e modos. Tambem confirma que partes essenciais da implementacao do
Bloco 2 permanecem abertas, sobretudo inicializacao de cursor/foco, algoritmo
detalhado de navegacao, registry completo de acoes e aplicacao do historico de
telas ao Enter do console.

O Bloco 3 permanece documentalmente separado por envolver selecao multipla,
toggle por espaco, conjunto de itens incluidos e uso comportamental de
`incluido_on`/`incluido_off`.

## 29. Encerramento literal

LEVANTAMENTO_CONCLUIDO
