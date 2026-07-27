---
name: H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico
description: Implementa a ADR-0031 - foco entre consoles focalizaveis, navegacao por setas, selecao unica, indicador de cursor derivado do estilo e chips condicionais [⇆]/[✥]
metadata:
  type: handoff
  handoff: H-0040
  adr_base: ADR-0031
  estado_inicial: BASE_DOCUMENTAL_APROVADA
  estado_final_esperado: HANDOFF_PATCHED_AWAITING_QA
---

# H-0040 - Implementar navegacao simples e selecao unica em console de nivel unico

## 1. Identificacao

| Campo | Valor |
|---|---|
| Numero | H-0040 |
| Titulo | Implementar navegacao simples e selecao unica em console de nivel unico |
| Origem | ITEM-0002 |
| ADR base | ADR-0031 - Navegacao simples e selecao unica em console de nivel unico |
| Estado inicial | `BASE_DOCUMENTAL_APROVADA` |
| Estado atual do handoff | `H1_HANDOFF_APPROVED` |
| Data | 2026-07-25 |

## 2. Estado processual e autoridade

```yaml
handoff:
  numero: H-0040
  status_anterior: HANDOFF_CRIADO_AGUARDANDO_QA
  status_apos_primeiro_patch: HANDOFF_PATCH_COMPLETED_AWAITING_QA
  status_apos_segundo_patch: HANDOFF_PATCH_COMPLETED_AWAITING_QA
  status_apos_patch_VM11: H1_HANDOFF_APPROVED

qa_inicial:
  relatorio: docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
  classificacao: H2_HANDOFF_PATCH_REQUIRED

primeiro_patch:
  etapa: PATCH_HANDOFF
  relatorio: docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
  achados_tratados:
    - QAH40-001
    - QAH40-002
    - QAH40-003
    - QAH40-004
    - QAH40-005
    - QAH40-006
    - QAH40-007
  nota_tratada:
    - QAH40-008

qa_pos_primeiro_patch:
  relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
  resultado_literal: H1_HANDOFF_APPROVED
  aceite_gerencial: REJEITADO_POR_INCONSISTENCIA_MATERIAL
  motivos:
    - provas_negativas_ainda_incompletas
    - validacao_manual_com_comandos_nao_executaveis
    - taxonomia_nao_canonica_residual

segundo_patch:
  etapa: SEGUNDO_PATCH_HANDOFF
  relatorio: docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
  achados_tratados:
    - SPH40-001
    - SPH40-002
    - SPH40-003

qa_pos_segundo_patch:
  executado: true
  relatorio: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md
  classificacao: H1_HANDOFF_APPROVED
  implementacao_liberada: true

implementacao:
  iniciada: true
  liberada: true
  relatorio: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  resultado_literal: IMPLEMENTATION_COMPLETED_AWAITING_QA

qa_implementacao:
  relatorio: docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
  patch_implementacao: docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
  qa_pos_patch_implementacao: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md

validacao_manual_primeira_rodada:
  resultado: NAO_APROVADA
  detalhe: historico_na_secao_23

ciclo_pos_validacao_manual:
  levantamento: docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md
  primeiro_patch_pos_validacao: docs/relatorios/RELATORIO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
  qa_pos_primeiro_patch_pos_validacao: I2_IMPLEMENTATION_PATCH_REQUIRED
  segundo_patch_pos_validacao: docs/relatorios/RELATORIO_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
  qa_pos_segundo_patch_pos_validacao:
    relatorio: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
    classificacao: I1_IMPLEMENTATION_APPROVED

validacao_manual_final:
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md
  resultado_global: FALHOU_PATCH_NECESSARIO
  VM_11: FALHOU

decisao_pos_validacao_manual:
  origem: DECISAO_EXPLICITA_DO_USUARIO
  metodo: IMPLEMENTACAO_INTEGRAL_DO_CENARIO
  nova_ADR: nao

  motivo:
    - VM-11 demonstrou falha real no recalculo da navegacao
    - o cenario de cinco itens foi insuficiente para validacao ampla
    - o usuario determinou um cenario maior e espacialmente observavel

  abordagem:
    - ampliar o proprio H-0040
    - autorizar configuracao JSON e codigo generico necessario
    - implementar e testar como uma unica entrega

patch_handoff_VM11:
  etapa: PATCH_HANDOFF
  motivo: incorporar_falha_VM11_e_ampliar_cenario_de_redimensionamento
  qa_inicial:
    relatorio: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0040.md
    resultado: H2_HANDOFF_PATCH_REQUIRED
  correcao_aplicada: true
  qa_pos_patch:
    relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0040.md
    resultado: H1_HANDOFF_APPROVED
  implementacao_liberada: true
  implementacao:
    relatorio: docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md
    resultado: IMPLEMENTATION_PATCH_COMPLETED
  qa_implementacao:
    relatorio: docs/relatorios/RELATORIO_QA_PATCH_VM-11_H-0040.md
    resultado: I1_IMPLEMENTATION_APPROVED
  validacao_manual:
    relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_POS_PATCH_VM-11_H-0040.md
    resultado: MANUAL_VALIDATION_APPROVED
```

A ADR-0031 e sua aplicacao documental permanecem aprovadas. A classificacao literal `H1_HANDOFF_APPROVED` do primeiro QA pos-patch nao foi aceita gerencialmente. O segundo patch do handoff foi aprovado pelo QA independente (`H1_HANDOFF_APPROVED`, `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md`) e liberou a implementacao, que foi executada, auditada e ajustada em dois ciclos de patch pos-validacao ate `I1_IMPLEMENTATION_APPROVED`. A validacao manual final (`docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md`) aprovou VM-01 a VM-10 e reprovou VM-11 por defeito real no recalculo da navegacao apos redimensionamento. Este terceiro patch corrige somente o handoff para incorporar a falha de VM-11 e a decisao do usuario de ampliar integralmente o cenario de redimensionamento; nao implementa e nao faz QA do H-0040.

### Validacao manual consolidada

```yaml
validacao_manual_consolidada:
  VM_01: APROVADO
  VM_02: APROVADO
  VM_03: APROVADO
  VM_04: APROVADO
  VM_05: APROVADO
  VM_06: APROVADO
  VM_07: APROVADO
  VM_08: APROVADO
  VM_09: APROVADO
  VM_10: APROVADO
  VM_11: FALHOU

  resultado_global: FALHOU_PATCH_NECESSARIO

  falha_VM_11:
    item_logico_preservado: true
    indicador_reposicionado: true
    geometria_visual_recalculada: true
    navegacao_recalculada: false
    classificacao: DEFEITO_DE_IMPLEMENTACAO
```

Os resultados de VM-01 a VM-10 permanecem preservados integralmente. A validacao manual futura deve repetir somente VM-11, com o roteiro revisado da Secao 23.

## 3. Origem e decisoes D1-D15

| Decisao | Sintese normativa |
|---|---|
| D1 | Escopo restrito a consoles de nivel unico ja expandidos. |
| D2 | Console focalizavel exige `politica_navegacao.navegavel: true` e ao menos um item navegavel. |
| D3 | Lista de foco por travessia em profundidade da arvore de corpo; grupos excluidos. |
| D4 | Ordem entre irmaos: horizontal esquerda-direita, vertical cima-baixo, matriz row-major. |
| D5 | Tab avanca e Shift+Tab recua circularmente na mesma lista. |
| D6 | Entrada em qualquer console posiciona cursor no item logico 0. |
| D7 | Itens navegaveis ordenados por row-major da grade visual vigente. |
| D8 | Celula vazia excluida do cursor e do toroide; eixo horizontal nao cruza linha e eixo vertical nao cruza coluna. |
| D9 | Linha ou coluna sem outro item ocupado no eixo produz `SEM_MOVIMENTO`. |
| D10 | Redimensionamento e mudanca de modo preservam item logico e recalculam posicao fisica. |
| D11 | Somente o console focado exibe indicador de cursor. |
| D12 | Indicador vem de `estilo.selecionado_simbolo`; linhas de continuacao recebem `selecionado_off`. |
| D13 | Selecao unica: item sob cursor e selecionado; sem toggle e sem indicador de inclusao. |
| D14 | [⇆] com ao menos dois consoles focalizaveis; [✥] somente no console focado com mais de um item navegavel. |
| D15 | Setas restritas a pagina atual; paginacao interativa deferida ao ITEM-0003. |

## 4. Escopo positivo

O implementador deve produzir a navegacao simples e selecao unica para consoles de nivel unico, cobrindo:

- lista ordenada de consoles focalizaveis;
- foco atual entre consoles;
- cursor por item logico dentro do console focado;
- Tab e Shift+Tab circulares;
- entrada sempre no item logico 0;
- navegacao horizontal por linha e vertical por coluna;
- toroide independente por eixo;
- exclusao de celulas vazias;
- preservacao do item logico em redimensionamento;
- preservacao do item logico em mudanca de modo;
- recalculo de linha, coluna e vizinhos na grade vigente;
- equivalencia entre grade usada pela navegacao e grade visual renderizada;
- selecao unica derivada do cursor;
- indicador somente no console focado;
- coluna indicadora estavel quando o cursor muda;
- indicador derivado do estilo global;
- chips [⇆] e [✥] por existencia contextual;
- correcao do recalculo de vizinhos e toroide imediatamente apos redimensionamento, antes do primeiro comando de seta (falha material de VM-11);
- cenario JSON com exatamente 26 itens navegaveis, formacao automatica dirigida por largura e altura correntes, distribuicao horizontal uniforme do espaco excedente e uma linha fisica em branco entre linhas da matriz;
- substituicao do cenario pequeno (`h0040_nav_console_grade_2x3.json`) como autoridade principal de VM-11 pelo novo cenario de 26 itens, preservando o cenario pequeno para provas de matriz incompleta e celulas vazias.

## 5. Escopo negativo

O implementador nao deve implementar, modificar ou introduzir:

- paginacao interativa por < e >;
- troca de pagina pelas setas;
- registro de acoes;
- dispatcher de acoes;
- Enter executando acao;
- nova resposta demonstrativa para Enter;
- abertura de outra tela;
- retorno por pilha;
- selecao multipla;
- toggle por espaco;
- indicador de inclusao;
- navegacao multinivel;
- expansao e recolhimento;
- conteudo composto e heterogeneo;
- alteracao funcional de dashboard;
- alteracao funcional de lancador;
- tela de escolha do estilo global;
- cores de alerta e inativo;
- tiling;
- cabecalho em largura reduzida;
- filtro por grupo;
- memoria de cursor por console;
- salto diagonal;
- compensacao de eixo ao encontrar celula vazia;
- busca pelo item geometricamente mais proximo;
- estado inativo de [✥];
- `regra_ativo` para [✥];
- navegacao entre paginas;
- alteracao das decisoes D1-D15 nao relacionada ao redimensionamento;
- nova familia de conteudo;
- estado de runtime persistido no JSON.

Ciclos futuros preservados: ITEM-0003, ITEM-0004, ITEM-0005, ITEM-0006, ITEM-0007, ITEM-0008 e ITEM-0009.

## 6. Inventario tecnico

| Arquivo | Evidencia inspecionada | Uso no handoff |
|---|---|---|
| `demo/demo.py` | `criar_estado_inicial`, `processar_comando`, `_ler_tecla_sessao`, SIGWINCH, modo verboso | Estado de runtime, teclado, demo TTY, redimensionamento e modo. |
| `demo/teste_demo.py` | estados manuais e comandos existentes | Regressao preservada; nao autorizado implicitamente. |
| `tela/loader.py` | validacao de `politica_navegacao`, `EstiloResolvido` | Fonte dos campos de navegacao e estilo. |
| `tela/modelo.py` | `ElementoCorpo._campos_inertes`, construcao recursiva | Fonte de itens, politica e arvore do corpo. |
| `tela/renderizador.py` | `_linhas_console`, `renderizar_tela`, chips | Superficie de indicador e chips. |
| `tela/distribuicao_matricial.py` | `calcular_distribuicao` | Fonte da geometria visual vigente. |
| `tela/teste_loader.py` | fixtures pre-ADR-0028 | Regressao de loader. |
| `tela/teste_renderizador.py` | renderizacao, distribuicao e modo verboso | Regressao de renderer. |

## 7. Arquivos modificaveis

```yaml
arquivos_modificaveis:
  total: 10
  lista:
    - arquivo: demo/demo.py
      responsabilidade: estado de runtime, teclado, demo TTY, redimensionamento e modos
      alteracao_autorizada: adicionar foco_console e cursores ao runtime; reconhecer Tab, Shift+Tab e setas; preservar Enter
    - arquivo: demo/demo_navegacao.py
      responsabilidade: sessao TTY interativa do H-0040
      alteracao_autorizada: suportar o novo cenario de 26 itens e o recalculo pos-redimensionamento
    - arquivo: demo/teste_demo_navegacao.py
      responsabilidade: testes de comando, estado e renderizacao integrada
      alteracao_autorizada: cobrir o cenario de 26 itens, as formacoes intermediarias e o recalculo imediato pos-redimensionamento
    - arquivo: tela/navegacao.py
      responsabilidade: API pura de foco, cursor, grade e selecao unica
      alteracao_autorizada: corrigir o recalculo de vizinhos e toroide imediatamente apos redimensionamento, antes do primeiro comando de seta
    - arquivo: tela/renderizador.py
      responsabilidade: renderizacao de tela, console, indicador e chips
      alteracao_autorizada: parametros opcionais de navegacao; indicador; regras dinamicas [⇆]/[✥]; suportar formacao automatica e distribuicao horizontal uniforme
    - arquivo: tela/distribuicao_matricial.py
      responsabilidade: calculo da geometria visual da matriz
      alteracao_autorizada: suportar formacao automatica dirigida por largura/altura correntes, distribuicao horizontal uniforme do excedente e separacao vertical de uma linha em branco entre linhas da matriz, sem quebrar as politicas ja contratadas
    - arquivo: tela/teste_navegacao.py
      responsabilidade: testes unitarios de navegacao pura
      alteracao_autorizada: cobrir o recalculo de vizinhos e toroide apos redimensionamento com o cenario de 26 itens
    - arquivo: tela/teste_renderizador.py
      responsabilidade: regressao de renderer
      alteracao_autorizada: cobrir a equivalencia entre grade renderizada e grade de navegacao no cenario de 26 itens
    - arquivo: tela/teste_distribuicao_matricial.py
      responsabilidade: regressao da distribuicao matricial
      alteracao_autorizada: cobrir formacao automatica, distribuicao horizontal uniforme e separacao vertical de uma linha em branco
    - arquivo: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
      responsabilidade: evidencia da implementacao do H-0040
      alteracao_autorizada: registrar a correcao do recalculo pos-redimensionamento e o novo cenario de 26 itens
```

Nenhum outro arquivo preexistente pode ser modificado sem acionar a regra de excecao.

## 8. Lista canonica dos 14 arquivos novos

```yaml
arquivos_novos:
  total: 14
  lista_canonica_unica: true

artefatos_canonicos_da_implementacao:
  total: 14
```

Este total de 14 corresponde a lista anterior de 13 artefatos acrescida de
`config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json`.

| Arquivo | Tipo | Finalidade | Consumidor nominal | Decisoes relacionadas |
|---|---|---|---|---|
| `tela/navegacao.py` | producao | API pura de foco, cursor, grade e selecao unica | `demo/demo.py`, testes | D2-D10, D13, D15 |
| `demo/demo_navegacao.py` | demo | Sessao TTY interativa do H-0040 | Usuario validador | D5, D10-D15 |
| `demo/teste_demo_navegacao.py` | teste | Testes de comando, estado e renderizacao integrada | `python -m pytest` | D5, D6, D10-D15 |
| `tela/teste_navegacao.py` | teste | Testes unitarios de navegacao pura | `python -m pytest` | D2-D10, D13, D15 |
| `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md` | relatorio futuro | Evidencia da implementacao | QA futuro | D1-D15 |
| `config/telas/demo/h0040_nav_console_unico_linear.json` | JSON demo | Um console focalizavel linear com quatro itens, incluindo item que ocupa multiplas linhas fisicas em modo verboso | `demo/demo_navegacao.py` | D2, D7, D12, D14 |
| `config/telas/demo/h0040_nav_dois_consoles.json` | JSON demo | Dois consoles focalizaveis; [⇆] presente; [✥] contextual | `demo/demo_navegacao.py` | D3-D6, D14 |
| `config/telas/demo/h0040_nav_tres_consoles_em_grupo.json` | JSON demo | Grupos aninhados e assimetricos; depth-first | `demo/demo_navegacao.py` | D3, D4 |
| `config/telas/demo/h0040_nav_console_grade_2x3.json` | JSON demo | Grade dinamica (preferencia_linhas): 2x3 incompleta em janela comum; redistribui ao estreitar; celulas vazias excluidas | `demo/demo_navegacao.py` | D7-D10 |
| `config/telas/demo/h0040_nav_console_nao_focalizavel.json` | JSON demo | Console nao navegavel ou vazio; chips ausentes | `demo/demo_navegacao.py` | D2, D14 |
| `config/telas/demo/h0040_nav_degenere_um_item.json` | JSON demo | Um item navegavel; [✥] ausente | `demo/demo_navegacao.py` | D9, D14 |
| `config/telas/demo/h0040_nav_degenere_uma_linha.json` | JSON demo | Um console com tres itens em uma linha; setas verticais produzem `SEM_MOVIMENTO` | `demo/demo_navegacao.py` | D8, D9 |
| `config/telas/demo/h0040_nav_degenere_uma_coluna.json` | JSON demo | Um console com tres itens em uma coluna; setas horizontais produzem `SEM_MOVIMENTO` | `demo/demo_navegacao.py` | D8, D9 |
| `config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json` | JSON demo | Matriz grande com exatamente 26 itens navegaveis; formacao automatica dirigida por largura/altura; distribuicao horizontal uniforme do espaco excedente; uma linha fisica em branco entre linhas da matriz; extremos `1x26` e `26x1`; substitui o cenario pequeno como autoridade principal de VM-11 | `demo/demo_navegacao.py` | D7-D10 |

Nenhum 15o arquivo novo fica previamente autorizado dentro desta lista fechada de 14 artefatos canonicos da implementacao. O relatorio `docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md` e autorizado nominalmente na subsecao "Relatorio processual autorizado para o patch VM-11" (Secao 33); e um relatorio processual do ciclo de patch de implementacao e nao integra esta lista fechada de 14, no mesmo padrao dos demais relatorios de patch e QA do ciclo.

```yaml
contagens:
  artefatos_canonicos_da_implementacao: 14
  cenarios_JSON: 9
  relatorio_processual_adicional: 1
```

Nao ha total agregado ambiguo de 15: os 14 artefatos canonicos da implementacao,
os 9 cenarios JSON de demonstracao (subconjunto ja contado dentro dos 14) e o
1 relatorio processual adicional do patch VM-11 sao contagens distintas e nao
se somam entre si.

## 9. Arquivos preservados

Devem permanecer preservados:

- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`
- `docs/relatorios/RELATORIO_QA_ADR-0031.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md`
- `docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md`
- `docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md`
- `docs/relatorios/RELATORIO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md`
- `docs/relatorios/RELATORIO_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md`
- `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md`
- `docs/backlog.md`
- `docs/adr/INDICE_ADR.md`
- `config/estilo.json`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`
- `demo/teste_demo.py`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/teste_loader.py`

`tela/distribuicao_matricial.py` e `tela/teste_renderizador.py` deixam de constar nesta lista de preservados e passam a constar em `arquivos_modificaveis` (Secao 7), autorizados nominalmente para suportar a formacao automatica, a distribuicao horizontal uniforme e a separacao vertical do cenario de 26 itens.

Nenhum arquivo listado como preservado aparece nas listas de modificar, criar ou condicional.

## 10. Arquivos condicionais

```yaml
arquivos_condicionais:
  total: 0
  lista: []
```

Nao ha autorizacao para substitutos genericos, ampliacoes implicitas, testes fora da lista, correlatos nao nominais ou escopo por pasta.

## 11. Regra operacional de excecao

```yaml
arquivo_fora_da_lista:
  acao: PARAR_ANTES_DA_ALTERACAO

  informar:
    - caminho_exato
    - responsabilidade_atual
    - motivo_da_necessidade
    - risco_de_nao_alterar
    - alteracao_minima_proposta
    - se_cria_nova_semantica

  aguardar_autorizacao_do_usuario: true
  alteracao_sem_autorizacao: proibida
```

A regra vale inclusive para teste existente, JSON existente, configuracao, demo, modulo de producao e relatorio nao previsto.

## 12. Consoles focalizaveis

Um console e focalizavel quando:

```text
tipo == "console"
AND politica_navegacao.navegavel == True
AND existe ao menos um item em _campos_inertes["itens"] com navegavel == True
```

`lancador`, `dashboard`, `grupo`, console nao navegavel e console navegavel sem item navegavel nunca entram na lista de foco. Consoles sem `_campos_inertes["itens"]` sao tratados como nao focalizaveis.

## 13. Lista de foco

A lista de foco e uma lista plana de consoles focalizaveis, construida por travessia em profundidade da arvore do corpo. Grupos sao percorridos, mas nao entram na lista. A ordem entre irmaos segue a declaracao visual: horizontal esquerda-direita, vertical cima-baixo e matriz row-major.

## 14. Tab e Shift+Tab

Tab (`"\t"`) avanca circularmente. Shift+Tab deve reconhecer as sequencias realmente recebidas no terminal alvo, testando `"\x1b[Z"` e `"\x1b\t"`, preservando Tab como tabulacao simples. Entrada em qualquer console sempre posiciona cursor no item logico 0. Lista de foco vazia nao altera o estado.

## 15. Grade, geometria e toróide

```yaml
fonte_da_geometria:
  navegacao: MESMO_RESULTADO_DA_EXIBICAO_ATUAL
  renderer: MESMO_RESULTADO_DA_EXIBICAO_ATUAL
  algoritmo_vigente: tela/distribuicao_matricial.py::calcular_distribuicao

grade_paralela_independente: proibida

identidade_logica:
  independente_da_posicao_visual: true

geometria_de_navegacao:
  depende_da_largura_atual: true
  depende_da_altura_atual: true
  deve_corresponder_a_grade_renderizada: true
```

O nome `grade_de_itens()` representa funcao nova autorizada em `tela/navegacao.py`. Ela deve consumir o mesmo resultado efetivamente usado pela exibicao atual. Celulas vazias sao `None`, nao recebem cursor e nao participam do toroide.

A falha material de VM-11 (Secao 2 e Secao 23) mostrou que esta equivalencia nao bastava: o defeito nao estava na geometria visual, que recalculava corretamente, mas no recalculo dos vizinhos e do toroide consumidos pela navegacao. A Secao 33 detalha o cenario de 26 itens e a correcao obrigatoria desse recalculo.

## 16. Cursor, selecao e indicador

O item sob cursor e o item selecionado. Nao ha conjunto de selecao, toggle por espaco ou indicador de inclusao. Somente o console focado exibe `estilo.selecionado_simbolo` na primeira linha fisica do item corrente. Linhas de continuacao e todos os itens nao correntes usam `estilo.selecionado_off`. A coluna indicadora permanece estavel quando o cursor muda.

## 17. Chips [⇆] e [✥]

```yaml
chips:
  "[⇆]":
    regra_existencia: tela_com_pelo_menos_dois_consoles_focalizaveis
    aparece_quando: len(lista_foco) >= 2
  "[✥]":
    regra_existencia: console_focado_com_mais_de_um_item_navegavel
    aparece_quando: console_focado possui mais de um item navegavel
    estado_inativo: proibido
```

Nos JSONs novos:

| JSON | [⇆] | [✥] | `regra_existencia` usada |
|---|---|---|---|
| `h0040_nav_console_unico_linear.json` | nao | sim | `console_focado_com_mais_de_um_item_navegavel`; cenario de item multilinha |
| `h0040_nav_dois_consoles.json` | sim | sim | ambas |
| `h0040_nav_tres_consoles_em_grupo.json` | sim | sim | ambas |
| `h0040_nav_console_grade_2x3.json` | nao | sim | `console_focado_com_mais_de_um_item_navegavel`; cenario de matriz incompleta |
| `h0040_nav_console_nao_focalizavel.json` | nao | nao | nenhuma |
| `h0040_nav_degenere_um_item.json` | nao | nao | nenhuma |
| `h0040_nav_degenere_uma_linha.json` | nao | sim | `console_focado_com_mais_de_um_item_navegavel` |
| `h0040_nav_degenere_uma_coluna.json` | nao | sim | `console_focado_com_mais_de_um_item_navegavel` |
| `h0040_nav_matriz_26_itens_redimensionamento.json` | nao | sim | `console_focado_com_mais_de_um_item_navegavel`; cenario principal de VM-11 |

## 18. Suite canonica

```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  comando_coleta: PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q
  coleta_na_autoria: 423
  natureza_da_contagem: COLETA_NO_MOMENTO_DA_AUTORIA
  contagem_pos_implementacao_pode_crescer: true
  resultado_exigido:
    falhas: 0
    erros: 0
```

O relatorio futuro deve registrar coletados, aprovados, ignorados, falhas, erros e comando executado. A contagem pos-implementacao nao e fixa em 423.

## 19. Criterios AT canonicos

Cada criterio deve possuir `id`, `decisao`, `superficie_observavel`, `teste_nominal` e `resultado_esperado`.

### AT-0001 - console focalizavel com item navegavel
`criterio: {id: AT-0001, decisao: D2, superficie_observavel: lista de foco, teste_nominal: teste_console_focalizavel_com_itens_navegaveis, resultado_esperado: console entra na lista}`
### AT-0002 - politica false exclui console
`criterio: {id: AT-0002, decisao: D2, superficie_observavel: lista de foco, teste_nominal: teste_console_nao_focalizavel_politica_false, resultado_esperado: console nao entra}`
### AT-0003 - zero itens navegaveis exclui console
`criterio: {id: AT-0003, decisao: D2, superficie_observavel: lista de foco, teste_nominal: teste_console_nao_focalizavel_sem_itens_navegaveis, resultado_esperado: console nao entra}`
### AT-0004 - lancador excluido
`criterio: {id: AT-0004, decisao: D1, superficie_observavel: lista de foco, teste_nominal: teste_lancador_nao_entra_lista_foco, resultado_esperado: lancador ausente}`
### AT-0005 - dashboard excluido
`criterio: {id: AT-0005, decisao: D1, superficie_observavel: lista de foco, teste_nominal: teste_dashboard_nao_entra_lista_foco, resultado_esperado: dashboard ausente}`
### AT-0006 - grupo estrutural percorre filhos
`criterio: {id: AT-0006, decisao: D3, superficie_observavel: lista de foco, teste_nominal: teste_grupo_estrutural_percorre_filhos, resultado_esperado: grupo ausente e filhos presentes}`
### AT-0007 - dois consoles planos em ordem
`criterio: {id: AT-0007, decisao: D3, superficie_observavel: lista de foco, teste_nominal: teste_lista_foco_dois_consoles_planos_ordem_declarada, resultado_esperado: ordem declarada}`
### AT-0008 - depth-first em grupos
`criterio: {id: AT-0008, decisao: D3, superficie_observavel: lista de foco, teste_nominal: teste_lista_foco_grupo_com_consoles_depth_first, resultado_esperado: filhos antes do console externo}`
### AT-0009 - irmaos horizontais
`criterio: {id: AT-0009, decisao: D4, superficie_observavel: lista de foco, teste_nominal: teste_lista_foco_irmaos_horizontais_esquerda_direita, resultado_esperado: esquerda para direita}`
### AT-0010 - matriz row-major
`criterio: {id: AT-0010, decisao: D4, superficie_observavel: lista de foco, teste_nominal: teste_lista_foco_irmaos_em_matriz_row_major, resultado_esperado: linhas antes de colunas}`
### AT-0011 - Tab avanca circular
`criterio: {id: AT-0011, decisao: D5, superficie_observavel: foco_console, teste_nominal: teste_tab_avanca_circular, resultado_esperado: ultimo avanca para primeiro}`
### AT-0012 - Shift+Tab recua circular
`criterio: {id: AT-0012, decisao: D5, superficie_observavel: foco_console, teste_nominal: teste_shift_tab_recua_circular_duas_sequencias, resultado_esperado: primeiro recua para ultimo}`
### AT-0013 - Tab sem foco
`criterio: {id: AT-0013, decisao: D5, superficie_observavel: foco_console, teste_nominal: teste_tab_sem_foco_foca_primeiro, resultado_esperado: indice zero}`
### AT-0014 - Shift+Tab sem foco
`criterio: {id: AT-0014, decisao: D5, superficie_observavel: foco_console, teste_nominal: teste_shift_tab_sem_foco_foca_ultimo, resultado_esperado: ultimo indice}`
### AT-0015 - Tab entra no item zero
`criterio: {id: AT-0015, decisao: D6, superficie_observavel: cursores, teste_nominal: teste_entrada_tab_cursor_item_zero, resultado_esperado: cursor zero}`
### AT-0016 - Shift+Tab entra no item zero
`criterio: {id: AT-0016, decisao: D6, superficie_observavel: cursores, teste_nominal: teste_entrada_shift_tab_cursor_item_zero, resultado_esperado: cursor zero}`
### AT-0017 - grade linear uma coluna
`criterio: {id: AT-0017, decisao: D7, superficie_observavel: grade de navegacao, teste_nominal: teste_grade_linear_uma_coluna_n_linhas, resultado_esperado: N linhas por uma coluna}`
### AT-0018 - grade visual row-major
`criterio: {id: AT-0018, decisao: D7, superficie_observavel: posicoes renderizadas, teste_nominal: teste_grade_distribuicao_matricial_row_major, resultado_esperado: indices seguem row-major}`
### AT-0019 - celula vazia marcada
`criterio: {id: AT-0019, decisao: D8, superficie_observavel: grade de navegacao, teste_nominal: teste_grade_celula_vazia_none, resultado_esperado: celula vazia e None}`
### AT-0020 - ordem linear preservada
`criterio: {id: AT-0020, decisao: D7, superficie_observavel: itens navegaveis, teste_nominal: teste_itens_console_linear_preserva_ordem, resultado_esperado: A B C viram 0 1 2}`
### AT-0021 - equivalencia grade navegacao e visual
`criterio: {id: AT-0021, decisao: D7, superficie_observavel: renderizacao e grade, teste_nominal: teste_grade_navegacao_equivale_grade_visual_vigente, resultado_esperado: mesmas linhas e colunas consumidas pelo renderer}`
### AT-0022 - seta direita toroide
`criterio: {id: AT-0022, decisao: D8, superficie_observavel: cursor, teste_nominal: teste_seta_direita_toroide, resultado_esperado: ultimo da linha vai ao primeiro da mesma linha}`
### AT-0023 - seta esquerda toroide
`criterio: {id: AT-0023, decisao: D8, superficie_observavel: cursor, teste_nominal: teste_seta_esquerda_toroide, resultado_esperado: primeiro da linha vai ao ultimo da mesma linha}`
### AT-0024 - seta baixo toroide
`criterio: {id: AT-0024, decisao: D8, superficie_observavel: cursor, teste_nominal: teste_seta_baixo_toroide, resultado_esperado: ultimo da coluna vai ao primeiro da mesma coluna}`
### AT-0025 - seta cima toroide
`criterio: {id: AT-0025, decisao: D8, superficie_observavel: cursor, teste_nominal: teste_seta_cima_toroide, resultado_esperado: primeiro da coluna vai ao ultimo da mesma coluna}`
### AT-0026 - celula vazia excluida na horizontal
`criterio: {id: AT-0026, decisao: D8, superficie_observavel: cursor, teste_nominal: teste_celula_vazia_excluida_toroide_horizontal, resultado_esperado: seta pula None sem cruzar linha}`
### AT-0027 - celula vazia excluida na vertical
`criterio: {id: AT-0027, decisao: D8, superficie_observavel: cursor, teste_nominal: teste_celula_vazia_excluida_toroide_vertical, resultado_esperado: seta pula None sem cruzar coluna}`
### AT-0028 - um item sem movimento
`criterio: {id: AT-0028, decisao: D9, superficie_observavel: cursor, teste_nominal: teste_um_item_qualquer_seta_sem_movimento, resultado_esperado: mesmo item}`
### AT-0029 - uma linha sem movimento vertical
`criterio: {id: AT-0029, decisao: D9, superficie_observavel: cursor, teste_nominal: teste_uma_linha_seta_vertical_sem_movimento, resultado_esperado: mesmo item}`
### AT-0030 - uma coluna sem movimento horizontal
`criterio: {id: AT-0030, decisao: D9, superficie_observavel: cursor, teste_nominal: teste_uma_coluna_seta_horizontal_sem_movimento, resultado_esperado: mesmo item}`
### AT-0031 - redimensionamento preserva item logico no cenario de 26 itens
`criterio: {id: AT-0031, decisao: D10, superficie_observavel: cursores e grade do cenario config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json, teste_nominal: teste_redimensionamento_preserva_item_logico, resultado_esperado: mesmo id logico preservado ao mudar entre ao menos quatro formacoes distintas, incluindo a passagem pelos extremos 1x26 e 26x1 em dimensoes controladas, sem retorno ao item 0}`
### AT-0032 - redimensionamento recalcula vizinhos no cenario de 26 itens
`criterio: {id: AT-0032, decisao: D10, superficie_observavel: linha coluna e vizinhos do cenario config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json, teste_nominal: teste_redimensionamento_recalcula_linha_coluna_vizinhos, resultado_esperado: vizinhos diferentes em formacoes diferentes; a primeira seta processada apos o redimensionamento usa a nova formacao; o retorno a uma formacao anterior restaura a vizinhanca correspondente; o toroide horizontal e vertical segue sempre a formacao atual}`
### AT-0033 - mudanca de modo preserva item logico
`criterio: {id: AT-0033, decisao: D10, superficie_observavel: cursores e renderizacao, teste_nominal: teste_mudanca_modo_preserva_item_logico, resultado_esperado: mesmo id logico em verboso e nao verboso}`
### AT-0034 - mudanca de modo recalcula grade atual
`criterio: {id: AT-0034, decisao: D10, superficie_observavel: grade e renderizacao, teste_nominal: teste_mudanca_modo_recalcula_grade_atual, resultado_esperado: posicoes fisicas atualizadas sem reiniciar item}`
### AT-0035 - indicador apenas no focado
`criterio: {id: AT-0035, decisao: D11, superficie_observavel: renderizacao, teste_nominal: teste_indicador_apenas_console_focado, resultado_esperado: simbolo so no console focado}`
### AT-0036 - indicador do estilo e coluna estavel
`criterio: {id: AT-0036, decisao: D12, superficie_observavel: coluna indicadora, teste_nominal: teste_indicador_simbolo_do_estilo_coluna_estavel, resultado_esperado: simbolo do estilo sem deslocar coluna}`
### AT-0037 - continuacoes recebem off
`criterio: {id: AT-0037, decisao: D12, superficie_observavel: renderizacao verbosa, teste_nominal: teste_continuacoes_recebem_selecionado_off, resultado_esperado: so primeira linha fisica recebe simbolo}`
### AT-0038 - selecao unica
`criterio: {id: AT-0038, decisao: D13, superficie_observavel: item selecionado, teste_nominal: teste_selecao_unica_cursor_eh_selecionado, resultado_esperado: selecionado e item sob cursor}`
### AT-0039 - chip alternar contextual
`criterio: {id: AT-0039, decisao: D14, superficie_observavel: barra de menus, teste_nominal: teste_chip_alternar_presente_dois_focalizaveis_ausente_um, resultado_esperado: [⇆] aparece so com dois ou mais focos}`
### AT-0040 - chip navegar contextual
`criterio: {id: AT-0040, decisao: D14, superficie_observavel: barra de menus, teste_nominal: teste_chip_navegar_presente_mais_de_um_item_ausente_um_item, resultado_esperado: [✥] aparece com mais de um item e some com um item}`

## 20. Provas PN canonicas

Cada prova deve possuir `id`, `proibicao`, `preparacao`, `estimulo`, `observacao`, `condicao_de_falha` e `teste_nominal`.

```yaml
PN:
  primeiro: PN-0001
  ultimo: PN-0017
  total: 17
  lacunas: 0
  duplicatas: 0
```

### PN-0001 - grupo nunca focalizavel
`prova: {id: PN-0001, proibicao: grupo estrutural na lista de foco, preparacao: grupo com filhos focalizaveis, estimulo: construir lista, observacao: tipos retornados, condicao_de_falha: tipo grupo retornado, teste_nominal: prova_grupo_nunca_na_lista_foco}`
### PN-0002 - lancador nunca focalizavel
`prova: {id: PN-0002, proibicao: lancador na lista de foco, preparacao: lancador no corpo, estimulo: construir lista, observacao: ids retornados, condicao_de_falha: lancador retornado, teste_nominal: prova_lancador_nunca_na_lista_foco}`
### PN-0003 - dashboard nunca focalizavel
`prova: {id: PN-0003, proibicao: dashboard na lista de foco, preparacao: dashboard no corpo, estimulo: construir lista, observacao: ids retornados, condicao_de_falha: dashboard retornado, teste_nominal: prova_dashboard_nunca_na_lista_foco}`
### PN-0004 - console nao navegavel ou sem itens excluido
`prova: {id: PN-0004, proibicao: console com politica nao navegavel ou sem item navegavel na lista de foco, preparacao: um console com navegavel false e outro com navegavel true sem itens navegaveis, estimulo: construir lista, observacao: lista de foco, condicao_de_falha: qualquer dos dois consoles aparece, teste_nominal: prova_console_nao_navegavel_ou_sem_itens_nunca_na_lista_foco}`
### PN-0005 - retorno nao restaura cursor anterior
`prova: {id: PN-0005, proibicao: retorno por Tab ou Shift+Tab restaurar cursor anterior, preparacao: ao menos dois consoles focalizaveis; cursor do primeiro fora do item 0; foco muda para outro console; retorno ao primeiro por Tab ou Shift+Tab, estimulo: Tab ou Shift+Tab de volta ao primeiro, observacao: cursor do console reentrado, condicao_de_falha: cursor anterior restaurado em vez de item logico 0, teste_nominal: prova_retorno_nao_restaura_cursor_anterior}`
### PN-0006 - celula vazia fora do cursor e do toroide
`prova: {id: PN-0006, proibicao: celula vazia receber cursor ou participar do toroide, preparacao: matriz incompleta com None entre itens, estimulo: seta horizontal e vertical com wrap, observacao: destino e sequencia de indices, condicao_de_falha: cursor em None ou movimento conta None como passo, teste_nominal: prova_celula_vazia_nao_recebe_cursor_nem_participa_toroide}`
### PN-0007 - eixo nao cruza linha nem coluna
`prova: {id: PN-0007, proibicao: movimento horizontal mudar de linha ou movimento vertical mudar de coluna, preparacao: item no fim da linha e item no fim da coluna, estimulo: seta direita e seta baixo, observacao: linha e coluna antes e depois, condicao_de_falha: linha mudou na horizontal ou coluna mudou na vertical, teste_nominal: prova_eixo_nao_cruza_linha_nem_coluna}`
### PN-0008 - indicador ausente em console nao focado
`prova: {id: PN-0008, proibicao: indicador aparecer em console nao focado, preparacao: ao menos dois consoles focalizaveis; somente um focado; ambos renderizados simultaneamente, estimulo: renderizar tela, observacao: selecionado_simbolo em cada console, condicao_de_falha: qualquer console nao focado exibe selecionado_simbolo, teste_nominal: prova_indicador_nao_aparece_em_console_nao_focado}`
### PN-0009 - [✥] ausente com um item
`prova: {id: PN-0009, proibicao: chip setas aparecer com exatamente um item navegavel, preparacao: console focado com um item, estimulo: renderizar barra, observacao: texto renderizado, condicao_de_falha: [✥] aparece, teste_nominal: prova_chip_navegar_nao_aparece_com_um_item}`
### PN-0010 - indicador fora da primeira linha
`prova: {id: PN-0010, proibicao: indicador aparecer em linha de continuacao, preparacao: item multilinha em modo verboso, estimulo: renderizar console focado, observacao: linhas fisicas, condicao_de_falha: simbolo em continuacao, teste_nominal: prova_indicador_nao_aparece_em_linha_de_continuacao}`
### PN-0011 - modo nao reinicia item
`prova: {id: PN-0011, proibicao: mudanca de modo reiniciar item zero, preparacao: cursor no item 2, estimulo: alternar modo, observacao: cursor antes e depois, condicao_de_falha: cursor vira 0, teste_nominal: prova_mudanca_modo_nao_reinicia_item_zero}`
### PN-0012 - redimensionamento nao perde identidade
`prova: {id: PN-0012, proibicao: redimensionamento perder identidade logica ou usar a formacao anterior antes da primeira seta, preparacao: cursor em item com grade larga no cenario de 26 itens, estimulo: recalcular grade estreita e processar a primeira seta, observacao: id logico, primeira seta processada e posicao visual versus posicao navegavel, condicao_de_falha: o item logico muda; o cursor volta ao primeiro item; a primeira seta usa a grade anterior; a posicao visual e a posicao navegavel divergem, teste_nominal: prova_redimensionamento_nao_perde_identidade_logica}`
### PN-0013 - Enter nao executa acao
`prova: {id: PN-0013, proibicao: Enter executar acao, preparacao: estado com item selecionado e contador de acoes, estimulo: processar Enter, observacao: estado e log de acoes, condicao_de_falha: acao registrada ou dispatcher chamado, teste_nominal: prova_enter_nao_executa_acao}`
### PN-0014 - seta nao muda pagina
`prova: {id: PN-0014, proibicao: seta alterar pagina, preparacao: pagina_atual observavel antes da seta, estimulo: quatro setas, observacao: pagina antes e depois, condicao_de_falha: pagina muda, teste_nominal: prova_setas_nao_mudam_pagina}`
### PN-0015 - indicador nao hardcoded
`prova: {id: PN-0015, proibicao: indicador hardcoded, preparacao: estilo com simbolo X, estimulo: renderizar cursor, observacao: saida, condicao_de_falha: aparece simbolo diferente do estilo, teste_nominal: prova_indicador_nao_hardcoded}`
### PN-0016 - grade de navegacao nao diverge da visual
`prova: {id: PN-0016, proibicao: grade de navegacao divergir da grade visual no cenario de 26 itens, preparacao: mesmo console, largura e altura, estimulo: calcular navegacao e renderizar em varias formacoes, observacao: coordenadas, celula do indicador, espacamento horizontal recalculado, linha em branco entre linhas e sobreposicao, condicao_de_falha: renderer e navegacao calculam formacoes diferentes; o indicador ocupa celula diferente da identidade selecionada; o espacamento horizontal nao e recalculado; a linha em branco obrigatoria desaparece; ocorre sobreposicao, teste_nominal: prova_grade_navegacao_nao_diverge_grade_visual}`
### PN-0017 - espaco nao alterna selecao
`prova: {id: PN-0017, proibicao: espaco alterar selecao, preparacao: estado com cursor, estimulo: processar espaco, observacao: selecao e cursores, condicao_de_falha: cria conjunto ou alterna inclusao, teste_nominal: prova_space_nao_togla_inclusao}`

## 21. Matriz de reconciliacao

| Identificador | Cobertura anterior | Cobertura apos segundo patch | Decisao | Teste nominal |
|---|---|---|---|---|
| AT-0021 | grade linear pequena | equivalencia entre grade de navegacao e grade visual | D7 | `teste_grade_navegacao_equivale_grade_visual_vigente` |
| AT-0031 | movimento horizontal | redimensionamento preserva item logico | D10 | `teste_redimensionamento_preserva_item_logico` |
| AT-0032 | indicador focado | redimensionamento recalcula linha, coluna e vizinhos | D10 | `teste_redimensionamento_recalcula_linha_coluna_vizinhos` |
| AT-0033 | indicador ausente | mudanca de modo preserva item logico | D10 | `teste_mudanca_modo_preserva_item_logico` |
| AT-0034 | simbolo do estilo | mudanca de modo recalcula grade atual | D10 | `teste_mudanca_modo_recalcula_grade_atual` |
| AT-0036 | estilo apenas | estilo e coluna indicadora estavel | D12 | `teste_indicador_simbolo_do_estilo_coluna_estavel` |
| AT-0040 | [✥] ausente | [✥] presente e ausente por contexto | D14 | `teste_chip_navegar_presente_mais_de_um_item_ausente_um_item` |
| PN-0004 | so politica false | politica nao navegavel e console sem item navegavel | D2 | `prova_console_nao_navegavel_ou_sem_itens_nunca_na_lista_foco` |
| PN-0005 | console sem itens | retorno por Tab/Shift+Tab sem restaurar cursor; entrada no item 0 | D6 | `prova_retorno_nao_restaura_cursor_anterior` |
| PN-0006 | destino nunca None | celula vazia nao recebe cursor e nao participa do toroide | D8 | `prova_celula_vazia_nao_recebe_cursor_nem_participa_toroide` |
| PN-0007 | so horizontal | horizontal nao muda linha e vertical nao muda coluna | D8 | `prova_eixo_nao_cruza_linha_nem_coluna` |
| PN-0008 | so vertical | indicador nao aparece em console nao focado | D11 | `prova_indicador_nao_aparece_em_console_nao_focado` |
| PN-0009 | cursor anterior | [✥] nao aparece com um item | D14 | `prova_chip_navegar_nao_aparece_com_um_item` |
| PN-0010 | [✥] sem inativo | indicador nao aparece em continuacao | D12 | `prova_indicador_nao_aparece_em_linha_de_continuacao` |
| PN-0011 | assinatura sem pagina | modo nao reinicia item zero | D10 | `prova_mudanca_modo_nao_reinicia_item_zero` |
| PN-0012 | espaco | redimensionamento nao perde identidade | D10 | `prova_redimensionamento_nao_perde_identidade_logica` |
| PN-0013 | indicador nao focado | Enter nao executa acao | D15 | `prova_enter_nao_executa_acao` |
| PN-0014 | [✥] sem foco | setas nao mudam pagina com pagina observavel | D15 | `prova_setas_nao_mudam_pagina` |
| PN-0016 | sem diagonal | grade de navegacao nao diverge da visual | D7/D8 | `prova_grade_navegacao_nao_diverge_grade_visual` |

### Reconciliacao adicional apos VM-11 (terceiro patch)

| Identificador | Cobertura apos segundo patch | Cobertura apos patch VM-11 | Decisao | Teste nominal |
|---|---|---|---|---|
| AT-0031 | preservacao do item logico apos redimensionar | preservacao do item logico no cenario de 26 itens, com ao menos quatro formacoes e passagem pelos extremos 1x26 e 26x1 | D10 | `teste_redimensionamento_preserva_item_logico` |
| AT-0032 | recalculo de linha, coluna e vizinhos | vizinhos diferentes por formacao; primeira seta pos-redimensionamento usa a nova formacao; retorno a formacao anterior restaura a vizinhanca; toroide segue a formacao atual | D10 | `teste_redimensionamento_recalcula_linha_coluna_vizinhos` |
| PN-0012 | identidade logica nao se perde ao redimensionar | id logico nao muda; cursor nao volta ao primeiro item; primeira seta nao usa a grade anterior; posicao visual e navegavel nao divergem | D10 | `prova_redimensionamento_nao_perde_identidade_logica` |
| PN-0016 | grade de navegacao nao diverge da visual | inclui espacamento horizontal recalculado, linha em branco obrigatoria entre linhas e ausencia de sobreposicao no cenario de 26 itens | D7/D8/D10 | `prova_grade_navegacao_nao_diverge_grade_visual` |

## 22. Demonstracao fechada

```yaml
demo:
  arquivo: demo/demo_navegacao.py
  ponto_de_entrada: main
  invocacao_base: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela
  Enter:
    alteracao_autorizada_neste_handoff: false
    nova_resposta_demonstrativa: proibida
    comportamento_preexistente: preservar
```

| Cenario | JSON exato | Comando exato | Comportamento visual observado |
|---|---|---|---|
| dois consoles | `config/telas/demo/h0040_nav_dois_consoles.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json` | Tab e Shift+Tab alternam o console focado; [⇆] aparece; indicador aparece somente no focado. |
| console nao focalizavel | `config/telas/demo/h0040_nav_console_nao_focalizavel.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_nao_focalizavel.json` | Tab nao aponta console; [⇆] e [✥] ausentes. |
| grupos assimetricos | `config/telas/demo/h0040_nav_tres_consoles_em_grupo.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_tres_consoles_em_grupo.json` | Ordem de foco segue depth-first por Tab e Shift+Tab. |
| matriz incompleta | `config/telas/demo/h0040_nav_console_grade_2x3.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json` | Quatro setas movem cursor por linha/coluna; celulas vazias nao recebem cursor; ao estreitar a janela a formacao muda e o item logico permanece. |
| um item | `config/telas/demo/h0040_nav_degenere_um_item.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_degenere_um_item.json` | Setas nao movem; [✥] ausente. |
| uma linha | `config/telas/demo/h0040_nav_degenere_uma_linha.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_degenere_uma_linha.json` | Setas verticais nao movem; setas horizontais mantem toroide na mesma linha. |
| uma coluna | `config/telas/demo/h0040_nav_degenere_uma_coluna.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_degenere_uma_coluna.json` | Setas horizontais nao movem; setas verticais mantem toroide na mesma coluna. |
| item multilinha e redimensionamento | `config/telas/demo/h0040_nav_console_unico_linear.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso` (item multilinha) e `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json` (redimensionamento) | Em modo verboso, somente a primeira linha fisica do item apontado recebe indicador. Maximizar, restaurar, reduzir e redimensionar livremente preservam item logico e recalculam posicao. |
| matriz de 26 itens e redimensionamento | `config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json` | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json` | Matriz grande, formacao automatica, distribuicao horizontal, separacao vertical, preservacao do item, recalculo dos vizinhos e toroide apos redimensionamento. |

## 23. Validacao manual futura

```yaml
validacao_manual:
  executante: USUARIO
  exclusiva_do_usuario: true
  executada_na_autoria_do_handoff: false
  executada_na_implementacao_automatica: false
```

Antes dos testes, explicar ao usuario:

- console focado: o quadro que esta recebendo os comandos do teclado;
- item apontado: a linha ou bloco marcado pela seta visual;
- chip: a indicacao de tecla mostrada na barra inferior.

```yaml
teste_manual:
  id: VM-01
  tela_ou_demo: dois consoles
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json
  tecla_ou_acao: Tab
  instrucao_em_linguagem_simples: passar para o proximo quadro
  resultado_visual_esperado: seta visual muda de quadro
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-02
  tela_ou_demo: tres consoles em grupo
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
  tecla_ou_acao: Tab e Shift+Tab
  instrucao_em_linguagem_simples: >
    Caso apareça o quadro de terminal pequeno, aumente a janela até os três
    consoles ficarem visíveis antes de iniciar o teste. Confirmar a ordem
    inicial dos tres consoles (console_a1, console_a2, console_externo). Com
    Tab, percorrer console_a1 → console_a2 → console_externo → console_a1. Com
    Shift+Tab, percorrer console_a1 → console_externo → console_a2 →
    console_a1. Confirmar circularidade e entrada no primeiro item de cada
    console ao focar.
  resultado_visual_esperado: >
    sentido direto e inverso distinguiveis; circularidade preservada;
    cada console inicia no item 0 ao receber o foco; sem sobreposicao
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-03
  tela_ou_demo: matriz incompleta 2x3
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json
  tecla_ou_acao: seta esquerda
  instrucao_em_linguagem_simples: mover o apontador para a esquerda
  resultado_visual_esperado: aponta item da mesma linha
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-04
  tela_ou_demo: matriz incompleta 2x3
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json
  tecla_ou_acao: seta direita
  instrucao_em_linguagem_simples: mover o apontador para a direita
  resultado_visual_esperado: aponta item da mesma linha
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-05
  tela_ou_demo: matriz incompleta 2x3
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json
  tecla_ou_acao: seta para cima
  instrucao_em_linguagem_simples: mover o apontador para cima
  resultado_visual_esperado: aponta item da mesma coluna
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-06
  tela_ou_demo: matriz incompleta 2x3
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json
  tecla_ou_acao: seta para baixo
  instrucao_em_linguagem_simples: mover o apontador para baixo
  resultado_visual_esperado: aponta item da mesma coluna
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-07
  tela_ou_demo: item multilinha em --verboso
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso
  tecla_ou_acao: abertura --verboso e navegacao por setas
  instrucao_em_linguagem_simples: >
    Abrir com --verboso (sem pressionar V). Localizar o item longo (Gamma...)
    com duas ou mais linhas fisicas. Confirmar indicador somente na primeira
    linha; linhas de continuacao sem indicador; navegar mantendo o modo
    verboso efetivo; confirmar item logico correto apos navegar. Nao esperar
    alternancia por V (cenario legada_sem_politica; V permanece no ciclo H-0037).
  resultado_visual_esperado: >
    item multilinha observavel; indicador na primeira linha; continuacoes sem
    indicador; modo verboso preservado apos setas/Tab/espaco; sem sobreposicao
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-08
  tela_ou_demo: redimensionamento
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json
  tecla_ou_acao: maximizar janela
  instrucao_em_linguagem_simples: ampliar a janela do terminal
  resultado_visual_esperado: mesmo item continua apontado
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-09
  tela_ou_demo: redimensionamento
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json
  tecla_ou_acao: restaurar janela
  instrucao_em_linguagem_simples: voltar a janela ao tamanho anterior
  resultado_visual_esperado: mesmo item continua apontado
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-10
  tela_ou_demo: matriz incompleta 2x3
  comando_de_abertura_exato: PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json
  tecla_ou_acao: reduzir janela ate a formacao mudar
  instrucao_em_linguagem_simples: >
    Abrir a matriz. Apontar um item que nao seja o primeiro. Estreitar a
    janela ate a quantidade de linhas ou colunas mudar. Confirmar que o
    mesmo item continua apontado. Confirmar que a seta acompanha a nova
    celula. Confirmar ausencia de seta em espaco vazio e de sobreposicao.
  resultado_visual_esperado: >
    formacao muda ao estreitar; item logico preservado; seta na nova celula;
    sem seta em espaco vazio; sem sobreposicao
  resposta_a_registrar: passou/falhou

teste_manual:
  id: VM-11
  tela_ou_demo: matriz_automatica_com_26_itens
  comando_de_abertura_exato: >
    PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao
    --tela config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  instrucao_em_linguagem_simples: >
    1. abra o cenario; 2. escolha um item distante do primeiro; 3. memorize a
    palavra selecionada; 4. aumente a largura ate obter a menor quantidade de
    linhas possivel; 5. estreite a largura ate obter a menor quantidade de
    colunas possivel; 6. passe por varias formacoes intermediarias; 7. confirme
    que a mesma palavra permanece apontada; 8. pressione as quatro setas em
    diferentes formacoes; 9. confirme que os vizinhos mudam de acordo com a
    formacao visivel; 10. confirme que a primeira seta apos cada
    redimensionamento ja usa a nova formacao; 11. confirme uma linha vazia
    entre linhas de elementos; 12. confirme que as colunas ocupam
    horizontalmente o espaco disponivel; 13. confirme ausencia de
    sobreposicao; 14. confirme ausencia de seta em espaco vazio.
  resultado_a_registrar:
    VM_11:
      resultado: APROVADO | FALHOU
      quantidade_de_itens_observada:
      menor_quantidade_de_linhas_observada:
      menor_quantidade_de_colunas_observada:
      formacoes_intermediarias_observadas:
      item_acompanhado:
      identidade_preservada:
      primeira_seta_usou_nova_formacao:
      vizinhos_recalculados:
      toroide_recalculado:
      linha_em_branco_entre_elementos:
      distribuicao_horizontal_uniforme:
      indicador_na_celula_correta:
      indicador_em_celula_vazia:
      sobreposicao:
      observacao:
```

O roteiro de VM-11 acima substitui integralmente o roteiro anterior, que usava o cenario pequeno `h0040_nav_console_grade_2x3.json`. A validacao manual futura deve repetir somente VM-11; os resultados aprovados de VM-01 a VM-10 permanecem preservados e nao precisam ser repetidos.

### Historico processual da validacao manual inicial

```yaml
validacao_manual_inicial:
  resultado: NAO_APROVADA
  VM_02: INCONCLUSIVO_POR_CENARIO
  VM_07: FALHOU_POR_ROTEIRO_E_OVERRIDE
  VM_10: APROVADO_COM_COBERTURA_FRACA
  VM_11: APROVADO_COM_COBERTURA_FRACA

levantamento_pos_validacao:
  classificacao: NO_NEW_ADR_PATCH_EXISTING_CYCLE

patch_pos_validacao:
  status: EXECUTADO_AGUARDANDO_QA

qa_pos_primeiro_patch_pos_validacao:
  classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
  achados:
    - QAPOSTVM40-001
    - QAPOSTVM40-002

segundo_patch_pos_validacao:
  status: EXECUTADO_AGUARDANDO_QA
  nova_ADR: false
  validacao_manual_executada: false
```

O `I1_IMPLEMENTATION_APPROVED` do QA tecnico pos-patch permanece como historico
anterior a validacao manual; nao libera o fechamento apos validacao manual
inconclusiva ou falha. O QA pos-primeiro-patch-pos-validacao classificou
`I2_IMPLEMENTATION_PATCH_REQUIRED` (QAPOSTVM40-001, QAPOSTVM40-002). O segundo
patch pos-validacao foi executado e aguarda QA; a nova validacao manual ainda
nao foi executada pelo usuario.

Preservados como corrigidos pelo primeiro patch pos-validacao:

```text
VM-07 roteiro
VM-07 override verboso
VM-07 item multilinha
VM-07 sobreposição
```

Etapa final obrigatoria: registrar o resultado da validacao manual em relatorio proprio ou no artefato documental definido pelo fluxo apos o QA automatizado.

### Resultado final consolidado da validacao manual

O segundo patch pos-validacao foi aprovado pelo QA tecnico (`I1_IMPLEMENTATION_APPROVED`,
`docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md`), o que
liberou a repeticao da validacao manual pelo usuario. O resultado final, registrado em
`docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md`, substitui as entradas fracas de
VM-10 e VM-11 do historico inicial:

```yaml
validacao_manual_final:
  VM_01: APROVADO
  VM_02: APROVADO
  VM_03: APROVADO
  VM_04: APROVADO
  VM_05: APROVADO
  VM_06: APROVADO
  VM_07: APROVADO
  VM_08: APROVADO
  VM_09: APROVADO
  VM_10: APROVADO
  VM_11: FALHOU
  resultado_global: FALHOU_PATCH_NECESSARIO
```

VM-11 revelou um defeito real de implementacao no recalculo dos vizinhos e do toroide
apos redimensionamento (Secao 2, `decisao_pos_validacao_manual`). Por decisao explicita
do usuario, o tratamento nao gera nova ADR: o proprio H-0040 foi ampliado neste terceiro
patch para autorizar o cenario de 26 itens (Secao 33) e a correcao obrigatoria do
recalculo (Secao 34), a serem implementados e testados como uma unica entrega.

## 24. Template do relatorio de implementacao

O implementador deve criar `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md` com template compativel com o fluxo vigente:

```yaml
resultado:
  etapa: IMPLEMENTAR_HANDOFF
  handoff: H-0040
  adr: ADR-0031

  arquivos_alterados:
  arquivos_criados:
  arquivos_preservados:
  arquivos_condicionais_acionados:
  excecoes_solicitadas:

  decisoes_implementadas:
    - D1
    - D2
    - D3
    - D4
    - D5
    - D6
    - D7
    - D8
    - D9
    - D10
    - D11
    - D12
    - D13
    - D14
    - D15

  criterios_AT:
    total: 40
    aprovados:
    falhos:

  provas_PN:
    total: 17
    aprovadas:
    falhas:

  suite_canonica:
    comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
    coletados:
    aprovados:
    ignorados:
    falhas:
    erros:

  demonstracao:
    arquivos:
    comandos:
    cenarios:
    resultado:

  validacao_manual_executada: nao

  operacoes_git_de_escrita_executadas: []
  commit_executado: nao
  bloqueios:

  encerramento: IMPLEMENTATION_COMPLETED_AWAITING_QA
```

A ultima linha futura do relatorio de implementacao deve ser `IMPLEMENTATION_COMPLETED_AWAITING_QA`. O relatorio nao aprova a propria implementacao.

## 25. Pontos NC

| Ponto | Classificacao | Tratamento |
|---|---|---|
| NC-001 | VERIFICACAO_TECNICA_NAO_BLOQUEANTE | Testar `"\x1b[Z"` e `"\x1b\t"`; reconhecer sequencias reais; preservar Tab como `"\t"`. |
| NC-002 | VERIFICACAO_TECNICA_NAO_BLOQUEANTE | `D23` e referencia de compatibilidade da ADR-0028/nomenclatura multinivel; estrutura real `ElementoCorpo._campos_inertes`; campo relevante `itens`; console sem item navegavel e `NAO_FOCALIZAVEL`. |
| NC-003 | DELIMITADO_PELO_PATCH | `grade_de_itens()` e funcao nova autorizada; usar mesmo resultado da exibicao atual; grade paralela independente proibida; exige AT e PN de equivalencia. |
| NC-004 | VERIFICACAO_TECNICA_NAO_BLOQUEANTE | `regra_existencia` ja e campo contratado; `campo_ja_contratado: true`; `mudanca_de_schema: false`; usar somente nos novos JSONs listados. |
| NC-005 | VERIFICACAO_TECNICA_NAO_BLOQUEANTE | Campos `foco_console` e `cursores` sao runtime; `persistir_no_JSON: false`; se `demo/teste_demo.py` precisar de mudanca, acionar excecao. |
| NC-006 | DELIMITADO_PELO_PATCH | Identidade logica independe da posicao visual; geometria depende da largura atual e deve corresponder a grade renderizada; grade independente do renderer proibida. |
| NC-007 | VERIFICACAO_TECNICA_NAO_BLOQUEANTE | `formacao.politica: preferencia_linhas` com `linhas.minimo: 1` e `linhas.maximo: 26` e a politica ja contratada em `tela/distribuicao_matricial.py` que produz os extremos `1x26` e `26x1` ao variar a formacao pela quantidade de linhas; o valor canonico de `distribuicao_horizontal.politica` e `uniforme` (Secao 33), ja vigente em contrato e loader, sem decisao pendente e sem introduzir nova politica fora das ja contratadas. |

## 26. Riscos e mecanismos

| Risco | Mecanismo associado |
|---|---|
| grade logica divergindo da visual | AT-0021, PN-0016 |
| Shift+Tab nao reconhecido | AT-0012, NC-001 |
| retorno restaurando cursor anterior | AT-0015, AT-0016, PN-0005 |
| perda da identidade do item | AT-0031, AT-0033, PN-0012 |
| hardcode do indicador | AT-0036, PN-0015 |
| indicador em console nao focado | AT-0035, PN-0008 |
| mudanca involuntaria de pagina | PN-0014, escopo negativo |
| regressao de largura util | AT-0032, NC-006 |
| chip exibido indevidamente | AT-0039, AT-0040, PN-0009 |
| campo de runtime persistido em JSON | NC-005, arquivos preservados, regra de excecao |
| arquivo novo excessivo | lista canonica de 14 artefatos canonicos da implementacao, regra de excecao |
| mistura entre nivel unico e multinivel | D1, NC-002, escopo negativo |
| Enter recebendo nova funcao | PN-0013, regra de Enter, escopo negativo |

## 27. Relatorio futuro e QA

O QA futuro da implementacao deve verificar: arquivos criados e modificados contra as listas canonicas, nenhuma alteracao nos preservados, excecoes formalmente autorizadas, AT e PN sem lacunas, suite canonica com zero falhas e zero erros, demonstracao fechada e validacao manual registrada somente pelo usuario.

## 28. Gate de entrada da implementacao

Antes de alterar codigo, o implementador deve confirmar:

```yaml
gate_de_entrada:
  handoff_status: HANDOFF_PATCH_COMPLETED_AWAITING_QA
  adr_0031_aceita: true
  relatorio_patch_handoff_presente: true
  suite_canonica_coleta:
    comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q
    natureza: coleta_informativa
  arquivo_tela_navegacao_preexistente:
    esperado: ausente
    se_presente: acionar_regra_de_excecao
```

## 29. Estado Git esperado apos implementacao

```yaml
estado_git_esperado:
  operacoes_git_de_escrita_executadas_pelo_implementador: []
  commit_executado: nao
  arquivos_modificados_autorizados:
    - demo/demo.py
    - tela/renderizador.py
  arquivos_novos_autorizados: 14
  arquivos_preservados: todos_os_demais
```

## 30. Checklist de QA minimo

```yaml
checklist_qa:
  - suite_canonica_zero_falhas_zero_erros
  - AT-0001_a_AT-0040_implementados_e_passando
  - PN-0001_a_PN-0017_implementadas_e_passando
  - demonstracao_nominal_executavel
  - validacao_manual_usuario_registrada_no_fluxo_posterior
  - nenhum_arquivo_nao_autorizado_sem_excecao
  - Enter_sem_nova_funcao
  - grade_navegacao_equivalente_grade_visual
  - chips_contextuais_sem_estado_inativo_para_[✥]
```

## 31. Dependencias futuras

| Item | Dependencia preservada |
|---|---|
| ITEM-0003 | Paginação interativa por [<][>] e troca de pagina fora do H-0040. |
| ITEM-0004 | Registro e execucao declarativa de acoes fora do H-0040. |
| ITEM-0005 | Abertura de outra tela e retorno por pilha fora do H-0040. |
| ITEM-0006 | Selecao multipla e toggle por espaco fora do H-0040. |
| ITEM-0007 | Navegacao multinivel e expansao/recolhimento fora do H-0040. |
| ITEM-0008 | Conteudo composto e heterogeneo fora do H-0040. |
| ITEM-0009 | Alteracao funcional de dashboard fora do H-0040. |

## 32. Decisoes deferidas preservadas

```yaml
decisoes_deferidas:
  ITEM-0003: paginacao_interativa_do_console
  ITEM-0004: registro_e_execucao_declarativa_de_acoes
  ITEM-0005: abertura_e_retorno_entre_telas
  ITEM-0006: selecao_multipla
  ITEM-0007: navegacao_multinivel_expansao_recolhimento
  ITEM-0008: conteudo_composto_e_heterogeneo
  ITEM-0009: dashboard_passivo
  DOC-B008: tipos_internos_de_item_de_console
  DOC-B009: registro_de_acoes_por_binding
  regra_ativo: avaliacao_de_estado_ativo_inativo_de_chips
```

## 33. Cenario matricial de 26 itens (patch VM-11)

Este cenario substitui `config/telas/demo/h0040_nav_console_grade_2x3.json` como
autoridade principal de VM-11. O cenario pequeno permanece preservado (Secao 9)
para provas de matriz incompleta e celulas vazias.

### Conteudo obrigatorio

```yaml
arquivo: config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
quantidade_itens: 26
ids: item_01 a item_26
palavras_por_item: 1
tamanho_minimo: 4
tamanho_maximo: 10
variacao_de_tamanho: obrigatoria
ordem_semantica: linha
todos_navegaveis: true
```

Conteudo, na ordem declarada:

```yaml
item_01: Lima
item_02: Nuvem
item_03: Cedro
item_04: Prisma
item_05: Bronze
item_06: Quartzo
item_07: Horizonte
item_08: Violeta
item_09: Jasmim
item_10: Cobalto
item_11: Marmore
item_12: Safira
item_13: Turquesa
item_14: Canario
item_15: Estrela
item_16: Planeta
item_17: Cometa
item_18: Nebulosa
item_19: Galaxia
item_20: Orquidea
item_21: Girassol
item_22: Magnolia
item_23: Alecrim
item_24: Bambu
item_25: Pessego
item_26: Cascata
```

### Configuracao matricial (nomenclatura canonica de `distribuicao_matricial`)

O JSON usa exclusivamente os campos ja contratados de `distribuicao_matricial`
(o mesmo bloco usado por `h0040_nav_console_grade_2x3.json`), com os valores
abaixo:

```yaml
distribuicao_matricial:
  formacao:
    politica: preferencia_linhas
    linhas: {minimo: 1, maximo: 26}
  ordem: por_linha
  dimensionamento:
    colunas: {politica: maior_da_coluna}
    linhas: {politica: maior_da_linha}
  espacamento:
    margem_esquerda: {minimo: 1}
    margem_direita: {minimo: 1}
    margem_superior: {minimo: 1, maximo: 1}
    margem_inferior: {minimo: 0, maximo: 0}
    vao_horizontal: {minimo: 2}
    vao_vertical: {minimo: 1, maximo: 1}
  distribuicao_horizontal: {politica: uniforme}
  distribuicao_vertical: {politica: inicio}
  ordem_expansao: {horizontal: uniforme_margens_e_vaos, vertical: uniforme_margens_e_vaos}
  politica_resto: {horizontal: ao_ultimo, vertical: ao_ultimo}
  alinhamento_interno: {horizontal: inicio, vertical: topo}
```

`formacao.politica: preferencia_linhas` com `linhas.minimo: 1` e `linhas.maximo: 26`
e a mesma politica ja usada em `h0040_nav_console_grade_2x3.json`; com `n_linhas`
variando de `1` a `26`, a primeira formacao geometricamente cabivel e a mais larga
(`1x26`, quando a largura permitir), avancando para mais linhas e menos colunas
conforme a largura estreita, ate o extremo `26x1`. `vao_vertical: {minimo: 1,
maximo: 1}` fixa exatamente uma linha fisica em branco entre linhas consecutivas
da matriz. `margem_superior: {minimo: 1, maximo: 1}` fixa uma linha de margem
superior; `margem_inferior: {minimo: 0, maximo: 0}` nao reserva margem inferior.

```yaml
politica_horizontal:
  valor_canonico: uniforme
  decisao_pendente: false
  capacidade_vigente: true
```

A politica horizontal deste cenario usa o valor canonico `uniforme`, ja vigente
em contrato e loader (Secao 25, NC-007); nao ha decisao pendente nem
placeholder de definicao futura pela implementacao.

Nao gravar no JSON: linhas calculadas, colunas calculadas, posicoes, vizinhos,
largura efetiva, altura efetiva, cursor, foco ou pagina calculada. Esses campos
sao runtime (NC-005) e nunca persistidos no JSON (D10, escopo negativo).

### Relatorio processual autorizado para o patch VM-11

```yaml
relatorio_patch_VM11:
  operacao_autorizada: criar
  finalidade:
    - registrar causa da falha manual
    - registrar correcao executada
    - registrar arquivos modificados
    - registrar testes automatizados
    - registrar ausencia de QA e validacao manual pelo implementador
  ultima_linha: IMPLEMENTATION_PATCH_COMPLETED
```

O relatorio `docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md` e autorizado
nominalmente para criacao nesta subsecao, com a finalidade acima e ultima linha
`IMPLEMENTATION_PATCH_COMPLETED`. Ele e um relatorio processual do patch de
implementacao e nao integra a lista fechada dos 14 artefatos canonicos da
implementacao (Secao 8) nem a contagem dos 9 cenarios JSON de demonstracao
(Secao 22, Secao 35):

```yaml
relatorio_processual:
  autorizado: true
  integra_contagem_dos_14_artefatos_canonicos: false
  integra_contagem_dos_9_cenarios: false
```

## 34. Formacao dinamica, distribuicao horizontal, separacao vertical e correcao da navegacao (patch VM-11)

### Formacao dinamica

```yaml
formacao:
  quantidade_de_itens: 26
  regra_horizontal:
    - usar a maior quantidade de colunas que caiba na largura atual
    - distribuir uniformemente o espaco horizontal excedente
    - recalcular os intervalos quando a largura mudar
  regra_vertical:
    - manter uma linha fisica vazia entre linhas consecutivas da matriz
    - considerar essa separacao no calculo da capacidade
    - recalcular a quantidade de linhas quando a altura mudar
  extremos:
    largura_suficiente: {formacao_esperada: 1x26}
    altura_suficiente_e_largura_minima: {formacao_esperada: 26x1}
  formacoes_intermediarias:
    obrigatorias: true
    exemplos: [2x13, 3x9, 4x7, 5x6, 7x4, 9x3, 13x2]
```

As formacoes intermediarias nao precisam ocorrer em dimensoes fixas, mas devem
ser produzidas quando houver espaco correspondente. Uma matriz final incompleta
e permitida.

### Distribuicao horizontal

```yaml
distribuicao_horizontal:
  largura_das_celulas: {origem: conteudo_da_coluna}
  espaco_excedente: {distribuicao: uniforme}
  intervalo_entre_colunas: {minimo: 2, dinamico: true}
  redimensionamento: {recalcular_intervalos: true, recalcular_posicoes: true}
```

Resultado visual esperado: colunas nao ficam acumuladas apenas a esquerda; o
espaco horizontal disponivel e utilizado; os intervalos entre colunas crescem e
diminuem com a janela; nao ocorre sobreposicao; nenhuma palavra e dividida
desnecessariamente; a variacao entre palavras de 4 a 10 letras permanece
observavel.

### Separacao vertical

```yaml
separacao_vertical:
  margem_superior: 1_linha
  entre_linhas_da_matriz: 1_linha_em_branco
  reserva_uniforme_por_item: proibida_quando_nao_necessaria
```

Cada linha logica da matriz deve ser separada da seguinte por exatamente uma
linha fisica vazia no cenario. A separacao pertence ao espacamento entre linhas
da matriz (`vao_vertical`). Nao deve ser produzida por conteudo vazio
artificial, item ficticio, altura inflada de todos os elementos, linhas
gravadas dentro do texto ou celulas falsas.

### Correcao da navegacao apos redimensionamento

```yaml
recalculo_apos_redimensionamento:
  preservar: [id_do_item_logico, console_focado, pagina_atual_quando_aplicavel, modo_atual]
  descartar: [linha_anterior, coluna_anterior, formacao_anterior, vizinhos_anteriores, largura_anterior, altura_anterior]
  recalcular: [formacao_atual, linha_atual, coluna_atual, vizinho_esquerdo, vizinho_direito, vizinho_superior, vizinho_inferior, retorno_toroidal]
  momento: [imediatamente_apos_mudanca_de_dimensao, antes_do_primeiro_comando_de_seta]
```

A primeira seta executada apos o redimensionamento deve usar a nova formacao.
Nao pode ser necessario trocar de console, pressionar Tab, mover antes para
outro item, reiniciar a tela ou sair e abrir novamente. Este e o defeito
material apontado por VM-11: a geometria visual recalculava corretamente, mas
os vizinhos e o toroide consumidos pela navegacao nao eram recalculados
(Secao 2, `validacao_manual_consolidada`).

### Testes espaciais obrigatorios

```yaml
formacoes_minimas: [1x26, 2x13, 4x7, 7x4, 13x2, 26x1]
verificacoes:
  - todos_os_26_itens_presentes
  - ordem_semantica_preservada
  - item_logico_preservado
  - indicador_na_celula_correta
  - vizinhos_recalculados
  - toroide_recalculado
  - uma_linha_em_branco_entre_linhas
  - espaco_horizontal_distribuido_uniformemente
  - ausencia_de_sobreposicao
  - ausencia_de_indicador_em_celula_vazia
```

Dimensoes concretas de terminal/janela devem ser descobertas e registradas pela
implementacao, nao fixadas previamente neste handoff.

### Regra de execucao integral

```yaml
regra_de_execucao:
  abordagem: INTEGRAL
  implementacao_parcial: nao_aceita
  fixture_especial_com_logica_hardcoded: proibida
  comportamento_generico_dirigido_por_JSON: obrigatorio
```

A implementacao nao pode: detectar o nome do arquivo H-0040 para mudar
comportamento; hardcodar 26 itens; hardcodar palavras; hardcodar dimensoes;
criar vizinhanca especifica para o cenario; produzir espacamento por strings
vazias; simular o recalculo apenas nos testes.

## 35. Checks mecanicos esperados

O patch documental deve permitir confirmar:

```yaml
AT:
  identificadores_unicos: 40
  menor: AT-0001
  maior: AT-0040
  lacunas: 0
  duplicatas: 0

PN:
  identificadores_unicos: 17
  menor: PN-0001
  maior: PN-0017
  lacunas: 0
  duplicatas: 0

arquivos_novos:
  total_nominal: 14

artefatos_canonicos_da_implementacao:
  total: 14

arquivos_modificaveis:
  total_nominal: 10

demonstracao:
  cenarios: 9

contagens:
  artefatos_canonicos_da_implementacao: 14
  cenarios_JSON: 9
  relatorio_processual_adicional: 1

suite_canonica: PYTHONDONTWRITEBYTECODE=1 python -m pytest
relatorio_implementacao_futuro: IMPLEMENTATION_COMPLETED_AWAITING_QA
```

## 36. Estado do repositorio no inicio do patch

```yaml
estado_git_inicial:
  arquivos_staged: []
  arquivos_unstaged:
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

### Estado do repositorio no inicio do patch VM-11 (terceiro patch)

```yaml
estado_git_inicial_patch_VM11:
  arquivos_staged: []
  arquivos_unstaged:
    - demo/demo.py
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  arquivos_nao_rastreados_relevantes:
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - tela/navegacao.py
    - tela/teste_navegacao.py
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/ (todos os relatorios historicos do ciclo H-0040 e ADR-0031)
  operacoes_git_de_escrita_executadas: []
  commit_executado: nao
```

`tela/distribuicao_matricial.py`, `tela/teste_renderizador.py` e
`tela/teste_distribuicao_matricial.py` nao aparecem como modificados neste
estado inicial: a autorizacao para modifica-los (Secao 7) vale para a proxima
implementacao, ainda nao executada por este patch documental.

## 37. Limite material deste terceiro patch

Este terceiro patch altera somente `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`. Nao cria nenhum relatorio nesta etapa (`relatorio_de_saida: nenhum`), nao executa novo QA, nao implementa o H-0040, nao cria fixtures, JSONs, testes, demos ou codigo, e nao executa operacoes Git de escrita. Os relatorios historicos do ciclo, incluindo `RELATORIO_QA_H-0040_HANDOFF.md`, `RELATORIO_PATCH_H-0040_HANDOFF.md`, `RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md`, `RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md`, `RELATORIO_IMPLEMENTACAO_H-0040.md` e `RELATORIO_VALIDACAO_MANUAL_H-0040.md`, permanecem preservados.

## 38. Resultado possivel apos QA independente

```yaml
resultado_possivel_apos_QA_independente:
  classificacao_de_aprovacao: H1_HANDOFF_APPROVED
  classificacao_nao_presumida_antes_do_QA: true
  bloqueantes_esperados: 0
  maiores_esperados: 0
  arquivos_nominais_novos: 14
  arquivos_nominais_modificaveis: 10
  AT:
    primeiro: AT-0001
    ultimo: AT-0040
    total: 40
  PN:
    primeiro: PN-0001
    ultimo: PN-0017
    total: 17
    lacunas: 0
    duplicatas: 0
```

O patch VM-11 do handoff foi avaliado por QA independente e aprovado com classificacao `H1_HANDOFF_APPROVED` (`docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0040.md`). A implementacao correspondente e a validacao manual pos-patch tambem ja foram comprovadas na cadeia existente.

## 39. Encerramento

```yaml
resultado: H1_HANDOFF_APPROVED
handoff: H-0040
adr: ADR-0031
qa_handoff_rejeitado: docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
relatorio_primeiro_patch: docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
qa_pos_primeiro_patch: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
aceite_gerencial_qa_pos_primeiro_patch: REJEITADO_POR_INCONSISTENCIA_MATERIAL
relatorio_segundo_patch: docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
qa_pos_segundo_patch: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md
classificacao_qa_pos_segundo_patch: H1_HANDOFF_APPROVED
implementacao: EXECUTADA_E_AUDITADA_ATE_I1_IMPLEMENTATION_APPROVED
validacao_manual_final: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md
resultado_validacao_manual_final: FALHOU_PATCH_NECESSARIO
VM_11: FALHOU
decisao_do_usuario_incorporada: true
nova_ADR_criada: nao
patch_atual: PATCH_HANDOFF_VM11
QA_deste_patch:
  executado: true
  qa_inicial: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0040.md
  resultado_inicial: H2_HANDOFF_PATCH_REQUIRED
  qa_pos_patch: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0040.md
  resultado_final: H1_HANDOFF_APPROVED
implementacao_deste_patch:
  executada: true
  relatorio: docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md
  resultado: IMPLEMENTATION_PATCH_COMPLETED
  QA_final: I1_IMPLEMENTATION_APPROVED
  qa_implementacao: docs/relatorios/RELATORIO_QA_PATCH_VM-11_H-0040.md
validacao_manual:
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_POS_PATCH_VM-11_H-0040.md
  resultado: MANUAL_VALIDATION_APPROVED
```

## 40. Marcador de estado

```yaml
handoff: H-0040
adr: ADR-0031
estado: H1_HANDOFF_APPROVED
suite_no_momento_da_autoria: 423_testes
data_segundo_patch: 2026-07-25
data_patch_VM11: 2026-07-26
```

H1_HANDOFF_APPROVED
