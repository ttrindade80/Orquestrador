---
name: relatorio-levantamento-compatibilidade-navegacao-distribuicao-console
description: Levantamento complementar sobre a vigencia de ec, tg e tx e compatibilidade entre navegacao e regras de distribuicao do console
metadata:
  type: relatorio
  etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
  escopo: Bloco_2_navegacao_selecao_unica_e_acoes
  status: corrigido
---

# Relatorio de Levantamento - Compatibilidade entre Navegacao e Distribuicao do Console

## 1. Identificacao

```yaml
etapa: LEVANTAMENTO_DOCUMENTAL_OU_ARQUITETURAL
papel: autor_responsavel_pela_correcao_factual
atividade_priorizada: Bloco_2_compatibilidade_navegacao_e_distribuicao
branch_informada: master
HEAD_informado: bab30c5
arquivo_corrigido: docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
```

## 2. Objetivo e limites

O objetivo deste levantamento complementar corrigido e registrar, sem nova pesquisa ampla, a compatibilidade factual entre a terminologia `ec`, `tg` e `tx` e as regras vigentes de distribuicao do console. A correcao remove conclusoes que excediam as evidencias ja coletadas e preserva a distincao entre terminologia, contratos, ADRs, configuracoes, implementacao e decisoes futuras.

Limites mantidos:

- Nao toma decisoes arquiteturais ou de implementacao.
- Nao propoe algoritmos ou solucoes de software.
- Nao cria ou altera ADRs, contratos, handoffs ou configuracoes existentes.
- Nao realiza QA do relatorio anterior.
- Nao altera `docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md`.
- Nao prepara stage, commit ou push no Git.

## 3. Decisao explicita de nao regressao

Fica registrada a decisao do usuario que rege a compatibilidade deste levantamento com desenvolvimento futuro:

```yaml
decisao:
  origem: USUARIO
  tema: nao_regressao_da_distribuicao
  regra: >
    A introducao de navegacao e selecao unica deve preservar as regras vigentes
    de agrupamento, matriz, cardinalidade, ocupacao, distribuicao, paginacao e
    redimensionamento consolidadas nos ciclos anteriores.
  proibicao: >
    Regras iniciais posteriormente modificadas nao podem ser reintroduzidas.
    ec, tg e tx nao podem ser usados para redefinir incidentalmente a geometria
    ou a distribuicao atual.
  limite: >
    Esta decisao comprova que o cursor nao pode redefinir nem degradar a
    geometria existente. Ela nao escolhe automaticamente qual estrutura o cursor
    usara para navegar.
```

## 4. Estado Git inicial

Antes da correcao factual, o estado observado no repositorio foi:

```text
$ git status --short --untracked-files=all
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md

$ git diff --name-status
(VAZIO)

$ git diff --cached --name-status
(VAZIO)

$ git diff --check
(VAZIO)
```

Registro factual corrigido:

```yaml
estado_antes_da_criacao_do_relatorio_complementar:
  workspace: UM_ARQUIVO_NAO_RASTREADO
  arquivo:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md

estado_no_inicio_da_correcao_factual:
  workspace: DOIS_ARQUIVOS_NAO_RASTREADOS
  arquivos:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
  alteracoes_rastreadas: nenhuma
  stage: VAZIO
```

Nao se usa `LIMPO` para workspace com arquivo nao rastreado.

## 5. Metodo de leitura seletiva

Esta correcao nao reaudita toda a documentacao. Ela preserva o material ja coletado no levantamento complementar e faz apenas ajustes factuais sobre cronologia, hierarquia documental, classificacoes e relacoes nao decididas.

## 6. Arquivos citados no levantamento

O levantamento complementar citou os seguintes artefatos como evidencias ou referencias:

1. `docs/INDICE.md`
2. `docs/adr/INDICE_ADR.md`
3. `docs/NOMENCLATURA.md`
4. `docs/nomenclatura/00_INDICE.md`
5. `docs/nomenclatura/10_ESTILO.md`
6. `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`
7. `docs/nomenclatura/32_CONSOLE.md`
8. `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`
9. `docs/contratos/contrato_console.md`
10. `docs/contratos/contrato_composicao_corpo.md`
11. `docs/contratos/contrato_json_console.md`
12. `docs/contratos/contrato_json_tela_minima.md`
13. `config/elementos/barra_de_menus.json`
14. `config/layouts/layout_console.json`
15. `config/layouts/layout_dado.json`
16. `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
17. `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md`
18. `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md`
19. `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`
20. `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`
21. `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
22. `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md`
23. `docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md`
24. `docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md`
25. `docs/handoff/H-0030-catalogo-telas-utilizaveis.md`
26. `docs/handoff/H-0033-ocupacao-integral-corpo.md`
27. `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
28. `docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md`
29. `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md`
30. `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
31. `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md`
32. `docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md`

## 7. Cronologia normativa corrigida

A cronologia anterior do relatorio era incompatível ao tratar a reorganizacao modular de 2026-07-21 como fase anterior aos ciclos H-0036/H-0037 de 2026-07-17/18. A versao corrigida separa origem de regra, materializacao modular e preservacao terminologica:

```yaml
data_de_origem_da_regra_ec_tg_tx: NAO_CONFIRMADA
data_de_materializacao_no_modulo_32: posterior_a_H0036_H0037
efeito_da_modularizacao: preservacao_ou_migracao_terminologica
superacao_pela_cronologia: NAO_COMPROVADA
```

Nao se usam `Fase 1` e `Fase 2` para classificar H-0036/H-0037 neste ponto, pois esses termos pertencem ao processo de aplicacao da ADR-0029 e nao comprovam anterioridade normativa de `ec`, `tg` e `tx`.

Registro temporal de H-0029:

```yaml
H_0029:
  tema: cardinalidade_unitaria
  relacao_com_ADR_0024: >
    A ADR-0024, criada posteriormente, consolidou regras compativeis de
    ocupacao integral; nao foi autoridade antecedente do H-0029.
```

Assim, preserva-se a diferenca entre origem historica do ajuste e autoridade normativa posterior que consolidou regra relacionada.

## 8. Hierarquia documental vigente

O estado vigente da documentacao de nomenclatura deve ser registrado assim:

```yaml
docs_NOMENCLATURA:
  natureza: FACHADA

docs_nomenclatura_00_INDICE:
  natureza: ROTEADOR

docs_nomenclatura_32_CONSOLE:
  natureza: AUTORIDADE_TERMINOLOGICA_VIGENTE

config_layouts_layout_console:
  natureza: CONFIGURACAO_OU_RASCUNHO_CONFORME_META_DO_PROPRIO_ARQUIVO
```

O eventual estado de `rascunho_inicial` de `config/layouts/layout_console.json` nao pode ser transferido automaticamente para `docs/nomenclatura/32_CONSOLE.md`. O modulo `32_CONSOLE.md` e autoridade terminologica vigente do dominio de console, enquanto contratos e ADRs mantem seus papeis proprios.

Hierarquia preservada:

- Modulos proprietarios sao autoridades terminologicas.
- Contratos sao autoridades comportamentais.
- ADRs sao autoridades das decisoes que formalizam.
- Implementacao material nao substitui automaticamente uma terminologia ativa.

## 9. Analise corrigida de `ec`, `tg` e `tx`

### 9.1 Ocorrencias ativas

O material coletado encontrou referencias ativas a `ec`, `tg` e `tx`, entre outras, em:

- `docs/nomenclatura/32_CONSOLE.md`
- `docs/nomenclatura/10_ESTILO.md`
- `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md`
- `docs/contratos/contrato_console.md`
- `config/elementos/barra_de_menus.json`
- `config/layouts/layout_console.json`
- `config/layouts/layout_dado.json`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md`

Estas ocorrencias confirmam atividade terminologica ou referencia documental. Elas nao devem ser promovidas automaticamente a implementacao operacional.

### 9.2 Campos persistidos e implementacao

A ausencia de `ec`, `tg` ou `tx` como campos persistidos no schema, ou como nomes internos do renderer, comprova apenas o seguinte:

```yaml
campos_persistidos_com_esses_nomes: nao
materializacao_operacional_com_esses_identificadores: nao_confirmada_ou_ausente
```

Ela nao comprova, por si so:

```yaml
terminologia_superada: true
regra_revogada: true
autoridade_historica: true
```

A ADR-0030 tambem registra decisoes ainda pendentes relacionadas a `tg` e `tx`. Portanto, a falta de consumo atual pode significar trabalho futuro, nao superacao.

### 9.3 Estado consolidado

```yaml
ec_tg_tx:
  autoridade_terminologica: CONFIRMADA
  autoridade_comportamental_especifica: PARCIAL_OU_NAO_CONFIRMADA
  campos_persistidos_no_json_estrutural: NAO
  campos_persistidos_no_conteudo_externo: NAO
  materializacao_fisica_atual_no_renderer: NAO_CONFIRMADA
  uso_como_geometria_global: PROIBIDO_PELA_DECISAO_DE_NAO_REGRESSAO
  superacao_explicita: NAO_ENCONTRADA
```

## 10. Separacao analitica entre camadas

Para fins deste levantamento, as evidencias foram separadas em quatro camadas analiticas, evitando usar uma camada como prova automatica de outra.

```yaml
modelo_de_dados_do_item:
  exemplos:
    - ec (termo terminologico)
    - tg (termo terminologico)
    - tx (termo terminologico)
    - campos_do_conteudo_externo
  estado: >
    ec, tg e tx permanecem termos do dominio de console. Os campos de conteudo
    externo seguem seus schemas e nao comprovam geometria fisica.

estado_interativo:
  exemplos:
    - cursor
    - item_em_foco
    - selecao_unica
    - pagina_atual
  estado: >
    Comportamentos de inicializacao, preservacao integral no redimensionamento,
    restauracao ao trocar cenario, persistencia em pilha, foco e cursor
    permanecem NAO_CONFIRMADOS quando a documentacao nao fecha explicitamente a
    regra.

estrutura_logica:
  exemplos:
    - grupos
    - itens_logicos
    - linhas_e_colunas_declaradas
    - coordenadas_de_grupo
  estado: >
    A documentacao comprova estruturas logicas e matrizes de grupos. Nao
    comprova automaticamente a ordem exata de navegacao do cursor.

geometria_renderizada:
  exemplos:
    - posicoes_finais
    - largura_e_altura
    - ocupacao_integral
    - distribuicao_responsiva
    - paginacao
  estado: >
    A geometria renderizada pertence ao calculo do renderer e as invariantes ja
    consolidadas de distribuicao. Ela nao revoga automaticamente terminologia
    ativa.
```

## 11. Invariantes vigentes de nao regressao

Qualquer desenvolvimento futuro da navegacao e selecao unica no console deve preservar as seguintes invariantes rastreaveis, sem atribuir ao cursor relacoes ainda nao decididas:

1. Matrizes de grupos declarativas e coordenadas explicitas continuam validas.
2. Cardinalidade unitaria continua ocupando integralmente a area disponivel.
3. Ocupacao integral horizontal e vertical permanece preservada.
4. Distribuicao responsiva permanece vigente.
5. Distribuicao matricial permanece vigente.
6. Conteudo externo continua separado do JSON estrutural e sem resultados geometricos persistidos.
7. Renderer mantem responsabilidade sobre geometria fisica, quebras, truncamento e paginacao.
8. Redimensionamento preserva as regras vigentes de recalculo da distribuicao.
9. Apresentacoes e modos multinivel permanecem intactos.
10. Telas existentes continuam compativeis.

Registro especifico sobre cursor e navegacao:

```yaml
navega_por_item_logico: DECIDIDO
ordem_exata_de_navegacao: NAO_CONFIRMADA
relacao_com_coordenadas_de_grupo: NAO_CONFIRMADA
relacao_com_posicoes_calculadas: NAO_CONFIRMADA
relacao_com_sequencia_visivel_da_pagina: NAO_CONFIRMADA
```

A decisao comprovada e que o cursor navega por itens, nao por linhas fisicas. O levantamento nao transforma isso automaticamente em navegacao pela ordem declarada do JSON, pelas coordenadas declaradas da matriz, pela sequencia visivel da pagina ou por reajuste especifico a uma nova grade.

## 12. Relacao decidida e relacoes abertas

Relacao decidida:

- O cursor navega por itens, nao por linhas fisicas.
- A navegacao nao pode degradar matriz de grupos, cardinalidade unitaria, ocupacao integral, distribuicao responsiva, distribuicao matricial, conteudo externo separado, responsabilidade do renderer, redimensionamento, apresentacoes e modos, nem compatibilidade das telas existentes.

Relacoes ainda abertas ou parcialmente abertas:

- Algoritmo detalhado de movimento do cursor em layouts matriciais 2D: `NAO_CONFIRMADO`.
- Tratamento detalhado de celulas vazias: `NAO_CONFIRMADO`.
- Ordem exata de navegacao: `NAO_CONFIRMADA`.
- Relacao do cursor com coordenadas de grupo: `NAO_CONFIRMADA`.
- Relacao do cursor com posicoes calculadas pelo renderer: `NAO_CONFIRMADA`.
- Relacao do cursor com sequencia visivel da pagina: `NAO_CONFIRMADA`.
- Primeiro item logico, elemento do corpo, foco ou cursor inicial: `NAO_CONFIRMADO`.
- Preservacao integral de cursor/foco ao redimensionar: `NAO_CONFIRMADO`.
- Restauracao de cursor/foco ao trocar cenario ou retornar por pilha: `NAO_CONFIRMADO`.
- Registry completo de acoes declarativas: `NAO_CONFIRMADO`.

## 13. Classificacao das formulacoes do relatorio anterior

```yaml
- formulacao: "Todo item navegavel do console tem ec, tg e tx, nessa ordem."
  autoridade_terminologica: CONFIRMADA
  materializacao_operacional: NAO_CONFIRMADA
  uso_como_geometria_global: PROIBIDO_PELA_DECISAO_DE_NAO_REGRESSAO
  classificacao: CONFIRMADA_COM_ESCOPO_LIMITADO
  limite: >
    A formulacao e terminologica para o item navegavel e nao define matriz do
    corpo, coordenadas do grupo, distribuicao do elemento, largura fixa
    obrigatoria ou geometria das apresentacoes multinivel.

- formulacao: "Item tem tres partes fixas."
  redacao_corrigida: >
    O modulo terminologico vigente declara tres partes, em ordem, para o item de
    console navegavel. Nao esta confirmado que essas partes sejam tres colunas
    fisicas fixas ou que determinem a geometria das apresentacoes multinivel.
  classificacao: CONFIRMADA_COM_ESCOPO_LIMITADO
  limite: >
    Nao ha ADR ou contrato citado que substitua explicitamente essa terminologia
    ou autorize classifica-la como SUPERADA.

- formulacao: "ec e o espaco do cursor."
  classificacao: CONFIRMADA_COM_ESCOPO_LIMITADO
  limite:
    - e definicao terminologica
    - recebe conceitualmente o indicador selecionado
    - nao define coordenada do grupo
    - nao define largura fisica fixa
    - materializacao operacional permanece futura ou nao confirmada

- formulacao: "tg e o espaco de toggle."
  classificacao: CONFIRMADA_COM_ESCOPO_LIMITADO
  limite:
    - e definicao terminologica
    - relaciona-se ao indicador incluido
    - comportamento de selecao multipla pertence ao Bloco 3
    - simbolo estatico para item navegavel sem selecao permanece pendente
    - nao deve ser imposto ao Bloco 2 como coluna geometrica obrigatoria
```

Registro especifico de `tx`:

```yaml
tx:
  autoridade_terminologica: VIGENTE
  regra_completa_de_ajuste: DEFERIDA_OU_NAO_CONFIRMADA
  materializacao_operacional: NAO_CONFIRMADA
  superacao: NAO_COMPROVADA
```

`tx` permanece termo terminologico para o texto do item. Regras completas de ajuste quando o texto nao cabe permanecem pendentes; essa pendencia nao significa revogacao do termo. A apresentacao multinivel tambem nao comprova substituicao de `tx`.

## 14. Riscos de regressao, sem superacao automatica

O risco comprovado nao e a existencia terminologica de `ec`, `tg` e `tx`, mas seu uso indevido como geometria global obrigatoria. Interpretar esses termos como colunas fisicas fixas para todas as apresentacoes poderia violar a decisao de nao regressao da distribuicao. Isso nao equivale a afirmar que os termos foram revogados ou que `32_CONSOLE.md` deixou de ser autoridade terminologica vigente.

## 15. Contradicoes

Nao se declara contradicao normativa ativa entre a nomenclatura `ec`/`tg`/`tx` e a arquitetura multinivel apenas porque a implementacao atual ainda nao materializa esses termos.

```yaml
contradicao_normativa_ativa_ec_tg_tx_vs_multinivel: NAO_CONFIRMADA
diferenca_entre_terminologia_e_implementacao: CONFIRMADA
superacao_explicita: NAO_ENCONTRADA
```

Uma ausencia de implementacao pode representar capacidade futura.

## 16. Matriz consolidada corrigida

| Tema | Autoridade ou evidencia | Estado corrigido | Efeito sobre navegacao |
|---|---|---|---|
| `ec` | `32_CONSOLE.md` e referencias ativas | CONFIRMADA_COM_ESCOPO_LIMITADO | Termo para espaco do cursor; nao define geometria global nem largura fixa. |
| `tg` | `32_CONSOLE.md` e referencias ativas | CONFIRMADA_COM_ESCOPO_LIMITADO | Termo para espaco de toggle; selecao multipla pertence ao Bloco 3 e nao deve ser imposta como coluna obrigatoria no Bloco 2. |
| `tx` | `32_CONSOLE.md` e referencias ativas | VIGENTE_COM_ESCOPO_LIMITADO | Termo para texto do item; ajuste completo permanece deferido ou nao confirmado. |
| estrutura do item | `32_CONSOLE.md` | CONFIRMADA_COM_ESCOPO_LIMITADO | Tres partes em ordem no plano terminologico; colunas fisicas fixas nao confirmadas. |
| ordem de navegacao | `contrato_console.md` citado no levantamento | PARCIALMENTE_DECIDIDA | Decidido apenas que o cursor navega por item logico, nao por linha fisica. |
| grupos e coordenadas | ADR-0020 e contrato de composicao | VIGENTE | Devem ser preservados; relacao exata com cursor permanece nao confirmada. |
| matriz | ADR-0020 | VIGENTE | Deve ser preservada sem regressao. |
| cardinalidade unitaria | H-0029; ADR-0024 posterior | VIGENTE | Deve ser preservada; ADR-0024 consolidou regra compativel posteriormente. |
| ocupacao integral | ADR-0024 e H-0033 | VIGENTE | Deve ser preservada sem fill externo indevido. |
| distribuicao responsiva | H-0034 | VIGENTE | Deve ser preservada; cursor nao redefine limiares. |
| distribuicao matricial | ADR-0025 e H-0035 | VIGENTE | Deve ser preservada. |
| conteudo multinivel | ADR-0026, ADR-0027, ADR-0028 | VIGENTE | Dados externos permanecem separados; isso nao revoga terminologia ativa. |
| redimensionamento | ADR-0017 | VIGENTE | Recalculo de distribuicao permanece; relacao especifica de cursor com nova grade e NAO_CONFIRMADA. |
| posicao fisica | ADR-0026 D11 | VIGENTE | Calculada pelo renderer; nao comprova revogacao de `ec`, `tg` ou `tx`. |
| cursor | `32_CONSOLE.md` e contrato de console | VIGENTE_COM_RELACOES_ABERTAS | Aponta item logico; inicializacao, persistencia e ordem exata permanecem nao confirmadas. |
| foco | contrato de console citado | VIGENTE_COM_RELACOES_ABERTAS | Alvo interativo; relacao estrita com cursor e persistencia permanece nao confirmada quando nao explicitada. |

## 17. Estado Git final

Ao concluir a correcao factual, o estado do repositorio foi confirmado com os mesmos comandos de diagnostico:

```text
$ git status --short --untracked-files=all
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md

$ git diff --name-status
(VAZIO)

$ git diff --cached --name-status
(VAZIO)

$ git diff --check
(VAZIO)
```

Estado final observado:

```yaml
arquivos_nao_rastreados:
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
arquivos_rastreados_modificados: nenhum
stage: VAZIO
git_diff_name_status: VAZIO
git_diff_cached_name_status: VAZIO
git_diff_check: VAZIO
```

## 18. Conclusao corrigida

Conclusao factual corrigida, sem decidir arquitetura:

1. `ec`, `tg` e `tx` permanecem terminologia ativa do dominio de console.
2. `ec`, `tg` e `tx` nao sao campos persistidos do JSON estrutural nem do conteudo externo.
3. A materializacao fisica atual de `ec`, `tg` e `tx` no renderer nao esta comprovada.
4. `ec`, `tg` e `tx` nao podem ser usados para redefinir a geometria consolidada.
5. A forma exata de apresentar o indicador de cursor sobre as apresentacoes atuais permanece decisao futura.
6. As regras de distribuicao e ocupacao dos ciclos anteriores sao invariantes.
7. A ordem e o algoritmo de navegacao continuam parcialmente abertos.
8. Ausencia de implementacao nao equivale a revogacao normativa.

RELATORIO_FACTUAL_CORRIGIDO
