---
name: ADR-0038-paginacao-interativa-limitada-em-console
description: "Fecha a paginação interativa do console (ITEM-0003): topologia limitada sem wrap entre páginas, cursor no primeiro item navegável da página de destino após troca explícita, páginas sem item navegável, universo por página do chip [✥], preservação de página no retorno por foco, repaginação por redimensionamento/modo, comportamento de filtros antes e depois da paginação, indicador página X/Y inclusive para conjunto vazio, independência de página por console e entradas aceitas para [<]/[>]"
metadata:
  type: adr
  status: aceita
  id: ADR-0038
  data: "2026-07-29"
  substitui: null
rastreabilidade:
  decisao_usuario: "D-PAG-01 a D-PAG-14 — topologia limitada (sem wrap entre primeira e última página); cursor no primeiro item navegável da página de destino após troca explícita de página, sem preservar posição física nem ordinal anterior; páginas com conteúdo visível e nenhum item navegável permanecem acessíveis e focadas, com controles de página ainda operáveis; universo de avaliação do chip [✥] restrito à página atual (especialização da regra de console focado da ADR-0031); retorno ao console por Tab/Shift+Tab preserva a página anterior do console sem restaurar o cursor anterior (especialização de ADR-0031 D6 para console paginado); redimensionamento e mudança de modo preservam o item lógico corrente e recalculam a página que passa a contê-lo; filtro que oculta o item corrente reposiciona o cursor no próximo item navegável da ordem lógica do conjunto filtrado, com fallback no item navegável anterior; filtro que resulta em zero itens navegáveis exibe a primeira página do resultado filtrado sem cursor visível; remoção de filtro não restaura o item anterior ao filtro, preservando a reconciliação já realizada; atualização genérica dos dados que remove o item corrente segue regra própria de fallback sem sobrescrever a reconciliação especializada por ID da ADR-0037; indicador página 1/1 sempre visível quando a paginação está habilitada, inclusive para conjunto com zero itens visíveis; página como estado independente por console, com comandos de página dirigidos exclusivamente ao console focado; entradas aceitas ',' e '<' para página anterior, '.' e '>' para próxima página, com chips [<] e [>]"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0003
    - ITEM-0018
  contratos_afetados:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
  handoffs_bloqueados: []
---

# ADR-0038 — Paginação interativa limitada em console

## 1. Status

`aceita`

```yaml
status_da_adr: aceita
qa_da_adr:
  resultado: ADR_APPROVED
  relatorio: docs/relatorios/RELATORIO_QA_ADR-0038.md
aplicacao_documental:
  executada: true
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0038.md
handoff:
  criado: true
  id: H-0045
implementacao:
  executada: true
  qa_final:
    resultado: I5_MANUAL_VALIDATION_REQUIRED
    relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P25.md
    suite_completa: 970_passed
validacao_manual:
  resultado: MANUAL_VALIDATION_APPROVED
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0045.md
commit_do_ciclo: nao_executado
```

Esta ADR foi criada a partir de 14 decisões fechadas fornecidas ao autor
documental (D-PAG-01 a D-PAG-14). Nenhuma delas foi escolhida, reaberta ou
alterada por este documento. O QA da ADR foi concluído com resultado
`ADR_APPROVED`, sem achados, e a aplicação documental propagou as decisões
aos contratos e módulos de nomenclatura afetados. O H-0045 foi criado e
implementado; o QA técnico final registrou `I5_MANUAL_VALIDATION_REQUIRED`
com 970 testes aprovados, restando somente a observação humana. A validação
manual TTY foi consolidada como `MANUAL_VALIDATION_APPROVED`, encerrando o
`ITEM-0003`. O commit do ciclo permanece reservado ao fechamento manual.

---

## 2. Contexto

### 2.1 Estado material ao início deste ciclo

A ADR-0031 formalizou foco, cursor lógico, navegação toroidal por eixo e
seleção única em console de nível único, mas excluiu explicitamente a
paginação interativa do seu escopo, registrando-a como fronteira de
compatibilidade e como atividade deferida ao `ITEM-0003` (ADR-0031 D15,
`contrato_console.md` §22.9). A ADR-0034 fechou a identidade e a persistência
da seleção múltipla entre páginas (D-SEL-01, D-SEL-10), mas também deferiu ao
`ITEM-0003` a paginação interativa em si e a prova de persistência de seleção
entre páginas. A ADR-0037 especializou o Handoff 4 do `ITEM-0006` sem alterar
essas fronteiras, mantendo a paginação da tela de resultado fora de escopo
(D-SEL-20).

Ao início deste ciclo:

- a paginação interativa do `ITEM-0003` ainda não está implementada;
- o cursor atual é um índice lógico global dos itens navegáveis do console
  (ADR-0031 D6, D7, D10);
- o runtime atual possui foco, cursores e seleções por console, mas não
  possui estado operacional de página;
- as setas não criam nem alteram página (ADR-0031 D8, D15;
  `contrato_console.md` §22.4);
- `config/telas/demo/demo.json` contém uma declaração antiga em objeto para
  `politica_paginacao`, mas esse arquivo é rascunho (`draft`) e esse formato
  não é adotado como schema por esta ADR.

Os contratos vigentes já preveem a existência estrutural de paginação —
`contrato_console.md` §12 declara paginação como consequência do conteúdo
que não cabe na área disponível, com página atual como estado de runtime não
pertencente ao JSON; `contrato_barra_de_menus.md` §8.3 declara `[<][>]` como
chips existentes quando a instância de `console` declara `paginacao: com`,
inativos quando há apenas uma página. Nenhum desses trechos fecha, porém, a
topologia entre páginas, o destino do cursor na troca, o comportamento de
páginas sem item navegável, o universo de avaliação do chip `[✥]` por página,
a preservação de página no retorno por foco, a repaginação por
redimensionamento ou mudança de modo, a interação entre filtro e página, o
indicador para conjunto vazio, a independência de página por console em
telas com múltiplos consoles, nem as entradas de teclado aceitas para
avançar ou retroceder página.

### 2.2 Problema

A ausência das regras acima impede a implementação de qualquer mecanismo de
paginação interativa no console, mesmo com as regras de navegação de nível
único já fechadas. Em particular, não havia resposta para:

1. A paginação é circular (última página avança para a primeira) ou
   limitada (primeira e última página têm bordas inativas)?
2. Ao trocar de página, o cursor preserva posição física, ordinal ou reinicia
   no primeiro item navegável da página de destino?
3. Uma página pode existir sem nenhum item navegável, mantendo conteúdo
   visível?
4. O chip `[✥]` avalia os itens navegáveis de toda a tela paginada ou somente
   da página atual?
5. Ao sair do console por Tab/Shift+Tab e retornar, a página é preservada ou
   reinicia?
6. Redimensionamento ou mudança de modo recalculam a página a partir de quê?
7. Um filtro que oculta o item corrente ou zera os itens navegáveis produz
   qual página e qual estado de cursor?
8. Remover um filtro restaura o item anterior ao filtro?
9. Uma atualização genérica dos dados que remove o item corrente segue a
   mesma regra de fallback da ADR-0037 para o retorno pós-execução real, ou
   é regra distinta?
10. Como o indicador de página se comporta com uma única página e com
    conjunto vazio?
11. Em tela com vários consoles, o estado de página é compartilhado ou
    independente, e quem recebe os comandos de página?
12. Quais entradas de teclado acionam página anterior e próxima página?

Esta ADR responde a essas questões por meio de 14 decisões fechadas
(D-PAG-01 a D-PAG-14).

### 2.3 Escopo positivo

```yaml
escopo_positivo:
  - topologia_entre_paginas
  - destino_do_cursor_apos_troca_explicita_de_pagina
  - pagina_sem_item_navegavel
  - universo_do_chip_navegar_por_pagina
  - preservacao_de_pagina_no_retorno_por_foco
  - repaginacao_por_redimensionamento_e_mudanca_de_modo
  - interacao_entre_filtro_e_paginacao
  - interacao_entre_atualizacao_generica_dos_dados_e_paginacao
  - indicador_pagina_x_de_y_inclusive_conjunto_vazio
  - independencia_de_pagina_por_console
  - entradas_aceitas_para_pagina_anterior_e_proxima_pagina
```

### 2.4 Escopo negativo

```yaml
escopo_negativo:
  - representacao_concreta_do_estado_de_paginas_em_classes_ou_dicionarios
  - nome_definitivo_de_novos_campos_de_runtime
  - schema_novo_de_politica_paginacao
  - algoritmo_fisico_de_quebra_de_paginas
  - estrutura_de_buffers
  - apis_classes_funcoes_ou_modulos
  - desempenho_cache_ou_renderizacao_parcial
  - paginacao_multinivel_colapsavel_do_item_0007
  - registry_generico_de_acoes
  - pilha_generica_de_telas
  - persistencia_entre_sessoes
  - alteracao_do_protocolo_focal_das_adrs_0034_a_0037
  - fixtures_e_roteiro_de_validacao_manual
  - lista_final_de_arquivos_de_implementacao
```

Esta ADR não reabsorve itens que pertencem a outros ciclos do backlog. A
seção 9 (Itens fora de escopo) detalha essa lista com a justificativa de
pertencimento de cada item.

### 2.5 Autoridades consultadas

| Documento | Papel |
|---|---|
| `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md` | Foco, cursor lógico, navegação toroidal por eixo, indicador, chips `[⇆]`/`[✥]`; D15 defere paginação ao `ITEM-0003` |
| `docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md` | Seleção como conjunto de IDs, persistência entre páginas, universo de `Todos` sobre o conjunto filtrado em todas as páginas |
| `docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md` | Origem suspensa, retorno de `dry-run` e retorno após execução real; reconciliação especializada por ID |
| `docs/contratos/contrato_console.md` | Estrutura da instância, navegação, seleção, filtros, paginação (§12), navegação/foco (§22), seleção múltipla e fluxo focal (§23) |
| `docs/contratos/contrato_chip.md` | Campos mínimos, tipos conceituais, regras de existência e de ativo/inativo do chip |
| `docs/contratos/contrato_barra_de_menus.md` | Ordem canônica, condições de existência de `[<][>]`, `[⇆]`, `[✥]` |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | Distinção entre configuração concreta e estado de runtime |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Terminologia de paginação, indicador de paginação, fronteiras de navegação simples (ADR-0031 D10, D15) |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Ordem fixa dos chips canônicos, condição de existência de `[<][>]`, `[⇆]`, `[✥]` |
| `docs/nomenclatura/32_CONSOLE.md` | Terminologia de console focalizável/focado, item lógico, wrap toroidal, paginação independente da navegação |

---

## 3. Decisão explícita do usuário

As 14 decisões abaixo são fechadas e transportadas integralmente. Nenhuma
alternativa é escolhida por este documento.

### D-PAG-01 — Topologia limitada

```yaml
topologia: LIMITADA
primeira_pagina:
  pagina_anterior: INATIVA
ultima_pagina:
  proxima_pagina: INATIVA
wrap_entre_paginas: false
```

Não há transição circular da primeira para a última página nem da última
para a primeira. Esta decisão fixa, para as páginas entre si, uma topologia
distinta da navegação toroidal por eixo dentro de uma mesma página (ADR-0031
D8, D9): dentro da página, o cursor faz wrap toroidal por linha e por
coluna; entre páginas, não há wrap.

### D-PAG-02 — Cursor após troca explícita de página

```yaml
evento: TROCA_EXPLICITA_DE_PAGINA
preservar_console_focado: true
cursor_destino: PRIMEIRO_ITEM_NAVEGAVEL_DA_PAGINA_DE_DESTINO
preservar_posicao_fisica: false
preservar_ordinal_da_pagina_anterior: false
```

A troca de página é uma transição de runtime dentro do mesmo console — não é
uma nova entrada por foco. O console permanece o mesmo console focado; apenas
sua página corrente muda. O cursor não preserva a posição física nem o
ordinal que ocupava na página anterior; ele é reposicionado no primeiro item
navegável da página de destino.

### D-PAG-03 — Página sem item navegável

```yaml
pagina_acessivel: true
exibicao: normal
console_permanece_focado: true
cursor_visivel: false
item_corrente: nenhum
setas: SEM_MOVIMENTO
controles_de_pagina: continuam_operaveis
pular_pagina_automaticamente: false
reorganizar_conteudo: false
```

Uma página pode conter conteúdo visível e nenhum item navegável. Essa página
permanece acessível e normalmente exibida; o console permanece focado; não
há cursor visível nem item corrente; as setas não produzem movimento; os
controles de página (`[<][>]`) continuam operáveis conforme sua própria
condição de existência e estado; o sistema não pula automaticamente para
outra página nem reorganiza o conteúdo para introduzir um item navegável
artificial.

### D-PAG-04 — Universo do chip `[✥]`

```yaml
universo_de_avaliacao: PAGINA_ATUAL
presente_quando: MAIS_DE_UM_ITEM_NAVEGAVEL_NA_PAGINA_ATUAL
ausente_quando:
  - ZERO_ITENS_NAVEGAVEIS_NA_PAGINA_ATUAL
  - UM_ITEM_NAVEGAVEL_NA_PAGINA_ATUAL
itens_em_outras_paginas_influenciam: false
```

Esta decisão especializa, para console paginado, a condição de existência de
`[✥]` já fixada pela ADR-0031 D14 (`console_focado_com_mais_de_um_item_
navegavel`; `contrato_console.md` §22.8; `contrato_barra_de_menus.md` §8.3).
A regra da ADR-0031 avaliava os itens navegáveis do console em foco sem
distinguir páginas — implicitamente, o console de nível único de então não
paginava. D-PAG-04 fecha essa lacuna: o universo relevante para a condição de
existência de `[✥]` é a página atual do console focado, não o total de itens
navegáveis do console em todas as páginas. Itens navegáveis presentes apenas
em outras páginas não fazem `[✥]` aparecer nem permanecer se a página atual
tiver zero ou um item navegável.

### D-PAG-05 — Retorno ao console por foco

```yaml
eventos:
  - RETORNO_POR_TAB
  - RETORNO_POR_SHIFT_TAB
pagina: PRESERVAR_PAGINA_ANTERIOR_DO_CONSOLE
restaurar_cursor_anterior: false
cursor_destino: PRIMEIRO_ITEM_NAVEGAVEL_DA_PAGINA_PRESERVADA
pagina_sem_item_navegavel:
  cursor_visivel: false
```

Cada console mantém seu estado de página durante a sessão. Esta decisão
especializa, para console paginado, a regra vigente de entrada no item
lógico global `0` (ADR-0031 D6, `contrato_console.md` §22.3): ao retornar por
Tab ou Shift+Tab a um console que já foi visitado, a página anterior desse
console é preservada — não há reinício na primeira página —, mas o cursor
não é restaurado ao item que ocupava antes da saída; o cursor é reposicionado
no primeiro item navegável da página preservada. Se a página preservada não
tiver item navegável (D-PAG-03), o cursor permanece sem exibição visível.

### D-PAG-06 — Repaginação por modo ou redimensionamento

```yaml
eventos:
  - REDIMENSIONAMENTO
  - MUDANCA_DE_MODO
preservar: ITEM_LOGICO_CORRENTE
pagina_apos_recalculo: PAGINA_QUE_PASSA_A_CONTER_O_ITEM_CORRENTE
preservar_numero_anterior_da_pagina: false
```

Identidade lógica é autoridade; número da página e posição física são
recalculados. Esta decisão estende às páginas o mesmo princípio que a
ADR-0031 D10 já fixa para redistribuição e mudança de modo dentro de uma
página (`contrato_console.md` §22.5): o item lógico corrente é preservado; a
página que passa a contê-lo após o recálculo pode ter número diferente do
anterior, e esse número anterior não é preservado como referência.

### D-PAG-07 — Filtro oculta o item corrente

```yaml
evento: FILTRO_OCULTA_ITEM_CORRENTE
destino_do_cursor:
  prioridade_1: PROXIMO_ITEM_NAVEGAVEL_NA_ORDEM_LOGICA_DO_CONJUNTO_FILTRADO
  prioridade_2: ITEM_NAVEGAVEL_ANTERIOR_SE_NAO_HOUVER_PROXIMO
pagina_resultante: PAGINA_QUE_CONTEM_O_NOVO_ITEM_CORRENTE
preservar_referencia_ao_item_oculto: false
```

Os filtros continuam sendo aplicados antes da paginação (`contrato_console.md`
§11, §12, R-4). Quando um filtro oculta o item que estava sob o cursor, o
cursor é reposicionado no próximo item navegável da ordem lógica do conjunto
já filtrado; se não houver próximo, no item navegável anterior dessa mesma
ordem. A página resultante é a que contém esse novo item corrente. Não há
memória de referência ao item ocultado para restauração futura.

### D-PAG-08 — Filtro deixa zero itens navegáveis

```yaml
evento: RESULTADO_FILTRADO_COM_ZERO_ITENS_NAVEGAVEIS
pagina_exibida: PRIMEIRA_PAGINA_DO_RESULTADO_FILTRADO
console_permanece_focado: true
cursor_visivel: false
item_corrente: nenhum
setas: SEM_MOVIMENTO
```

O resultado ainda pode possuir conteúdo visível não navegável. Quando o
conjunto filtrado não contém nenhum item navegável, a primeira página desse
resultado filtrado é exibida; o console permanece focado; não há cursor
visível nem item corrente; as setas não produzem movimento.

### D-PAG-09 — Remoção do filtro

```yaml
evento: REMOCAO_DE_FILTRO
restaurar_item_anterior_ao_filtro: false
preservar: ITEM_LOGICO_CORRENTE_APOS_RECONCILIACAO
pagina_resultante: PAGINA_QUE_CONTEM_O_ITEM_CORRENTE_ATUAL
memoria_especial_de_cursor_por_filtro: ausente
```

Remover o filtro não desfaz a reconciliação já realizada por D-PAG-07 ou
D-PAG-08. O item logicamente corrente após essa reconciliação é preservado;
a página resultante é a que contém esse item corrente atual; não existe
memória especial de cursor por filtro para restaurar o item que era corrente
antes do filtro ter sido aplicado.

### D-PAG-10 — Atualização remove o item corrente

```yaml
evento: ATUALIZACAO_GENERICA_DOS_DADOS_REMOVE_ITEM_CORRENTE
destino_do_cursor:
  prioridade_1: PROXIMO_ITEM_NAVEGAVEL_COM_BASE_NA_POSICAO_LOGICA_ANTERIOR
  prioridade_2: ITEM_NAVEGAVEL_ANTERIOR_SE_NAO_HOUVER_PROXIMO
pagina_resultante: PAGINA_QUE_CONTEM_O_NOVO_ITEM_CORRENTE
sem_itens_navegaveis:
  pagina: PRIMEIRA
  cursor_visivel: false
```

Esta é a regra genérica de atualização dos dados. Ela não substitui
automaticamente a regra especializada da ADR-0037 para retorno após execução
real (D-H4-09, `contrato_console.md` §23.9): no fluxo especializado da
ADR-0037, permanece a reconciliação por ID do item anterior — se esse ID
continuar válido, o cursor é preservado nele; caso contrário, o fallback é o
primeiro item navegável, não o "próximo item navegável com base na posição
lógica anterior" de D-PAG-10. D-PAG-10 aplica-se a atualizações genéricas de
dados fora do fluxo focal de execução real da ADR-0037; onde os dois
conjuntos de regras poderiam se sobrepor, prevalece a regra especializada da
ADR-0037, sem conflito declarado entre as duas: D-PAG-10 é a regra padrão do
`ITEM-0003` para o caso geral; a regra da ADR-0037 é especialização exclusiva
do Handoff 4 do `ITEM-0006` e não é redefinida por esta ADR.

### D-PAG-11 — Indicador em console com uma página

```yaml
uma_pagina:
  indicador: "página 1/1"
  pagina_anterior: INATIVA
  proxima_pagina: INATIVA
```

Quando a paginação estiver habilitada na instância de `console`, o indicador
é sempre visível — inclusive quando há apenas uma página. Nesse caso, os
chips `[<]` e `[>]` existem (a instância declara paginação) mas permanecem
inativos, conforme já previsto por `contrato_barra_de_menus.md` §8.3
("Inativo quando há apenas 1 página no momento").

### D-PAG-12 — Conjunto com zero itens visíveis

```yaml
quantidade_de_itens_visiveis: 0
pagina_logica:
  atual: 1
  total: 1
indicador: "página 1/1"
pagina_anterior: INATIVA
proxima_pagina: INATIVA
cursor_visivel: false
item_corrente: nenhum
```

Não existe estado visual `página 0/0`. Quando o conjunto de itens visíveis é
zero — inclusive quando decorrente de filtro (D-PAG-08) —, a paginação
lógica permanece em página `1` de `1`, o indicador exibe `página 1/1`, e
`[<]`/`[>]` permanecem inativos.

### D-PAG-13 — Vários consoles na mesma tela

```yaml
estado_de_pagina: INDEPENDENTE_POR_CONSOLE
alvo_dos_comandos_de_pagina: CONSOLE_FOCADO
sem_console_focado:
  pagina_anterior: INATIVA
  proxima_pagina: INATIVA
console_focado_sem_paginacao:
  pagina_anterior: INATIVA
  proxima_pagina: INATIVA
console_focado_com_paginacao:
  estado_dos_controles: CALCULADO_PELA_PAGINA_DESSE_CONSOLE
alterar_outros_consoles: false
alterar_foco: false
```

O estado de página é independente por console — análogo à independência já
fixada para a seleção múltipla pela ADR-0034 (D-SEL-01). Os comandos de
página (D-PAG-14) são dirigidos exclusivamente ao console focado. Sem
console focado, ou com o console focado sem paginação declarada, `[<]` e
`[>]` permanecem inativos. Com o console focado paginando, o estado dos
controles é calculado a partir da página desse console, sem alterar o estado
de página de nenhum outro console nem alterar o foco corrente. A existência
declarativa dos chips (`regra_existencia`, estática, derivada da declaração
no `tela.json` — `contrato_chip.md` §8) e sua ativação dinâmica
(`regra_ativo`, recalculada a cada render — `contrato_chip.md` §9)
permanecem conceitos distintos: a existência de `[<][>]` depende de a
instância declarar `paginacao: com`; o estado ativo/inativo depende da
página corrente do console focado no momento do render.

### D-PAG-14 — Entradas aceitas

```yaml
pagina_anterior:
  entradas_aceitas:
    - ","
    - "<"
proxima_pagina:
  entradas_aceitas:
    - "."
    - ">"
chips_exibidos:
  anterior: "[<]"
  proxima: "[>]"
```

As entradas aceitas para acionar página anterior e próxima página são os
caracteres acima. Esta decisão não define leitura por scan code, keycode
físico nem dependência de layout de teclado — a fronteira de captura e
tradução de tecla física para o caractere lógico permanece de implementação,
fora do escopo desta ADR. Os chips exibidos permanecem `[<]` e `[>]`,
consistentes com a notação documental já vigente em
`contrato_barra_de_menus.md` §7 e §8.3 e em
`docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` §4.3.

---

## 4. Decisão

Fica adotado, para o `ITEM-0003`, um modelo de paginação interativa do
console organizado em quatro camadas, todas fechadas por decisão explícita
do usuário e sem alternativa de desenho em aberto:

**Topologia e transição entre páginas (D-PAG-01, D-PAG-02).** A paginação é
limitada, não circular: a primeira página não tem página anterior operável e
a última não tem próxima página operável. Toda troca explícita de página é
uma transição de runtime dentro do mesmo console focado, que reposiciona o
cursor no primeiro item navegável da página de destino, sem preservar
posição física ou ordinal da página anterior.

**Página como domínio fechado da navegação por setas, inclusive quando vazia
de itens navegáveis (D-PAG-03, D-PAG-04).** Cada página permanece um domínio
fechado para as setas — regra já fixada pela ADR-0031 (D8, D9, D15) e agora
estendida ao conceito de página como unidade de paginação interativa. Uma
página pode exibir conteúdo sem ter item navegável, permanecendo acessível e
com controles de página operáveis; o console permanece focado, sem cursor
visível. O universo de avaliação do chip `[✥]` — especialização de ADR-0031
D14 — passa a ser a página atual do console focado, não o console inteiro em
todas as páginas.

**Página como estado de runtime independente por console, preservado no
retorno por foco e recalculado por redimensionamento, mudança de modo,
filtro e atualização de dados (D-PAG-05 a D-PAG-10, D-PAG-13).** A página é
estado de runtime, independente por console — mesmo princípio de
independência já fixado para foco (ADR-0031) e seleção múltipla (ADR-0034).
O retorno por Tab/Shift+Tab preserva a página anterior do console, sem
restaurar o cursor anterior — especialização de ADR-0031 D6 para console
paginado. Redimensionamento e mudança de modo preservam o item lógico
corrente (ADR-0031 D10) e recalculam a página que passa a contê-lo, sem
preservar o número anterior da página. Filtros continuam sendo aplicados
antes da paginação (`contrato_console.md` R-4); quando ocultam o item
corrente ou zeram os itens navegáveis, o cursor e a página são reconciliados
segundo prioridade determinística; a remoção do filtro não desfaz essa
reconciliação. A atualização genérica dos dados que remove o item corrente
segue regra própria de fallback (D-PAG-10), que não substitui nem é
substituída pela reconciliação especializada por ID já fixada pela ADR-0037
para o retorno após execução real do Handoff 4 do `ITEM-0006` — as duas
regras coexistem em fronteiras distintas, sem contradição. Em tela com
múltiplos consoles, o estado de página é independente por console e os
comandos de página são dirigidos exclusivamente ao console focado, sem
alterar outros consoles nem o foco corrente.

**Indicador, chips e entradas aceitas (D-PAG-11, D-PAG-12, D-PAG-14).** O
indicador `página X/Y` é sempre visível quando a paginação está habilitada,
inclusive com uma única página (`página 1/1`, controles inativos) e com
conjunto vazio de itens visíveis (`página 1/1`, controles inativos, sem
cursor). Não existe estado visual `página 0/0`. As entradas de teclado
aceitas para página anterior são `,` e `<`; para próxima página, `.` e `>`;
os chips exibidos permanecem `[<]` e `[>]`.

Esta decisão não redefine a topologia toroidal por eixo dentro de uma página
já fixada pela ADR-0031, não redefine a identidade nem a persistência da
seleção múltipla entre páginas já fixadas pela ADR-0034, e não redefine o
protocolo focal de execução, a tela padrão de resultado nem a reconciliação
especializada por ID do retorno após execução real já fixados pela ADR-0034,
ADR-0035, ADR-0036 e ADR-0037.

---

## 5. Consequências

### Positivas

- Fecha a lacuna operacional deixada explicitamente pela ADR-0031 (D15) para
  paginação interativa, permitindo avançar o `ITEM-0003` para handoff de
  implementação em ciclo próprio.
- Desbloqueia parcialmente o `ITEM-0018` (`Selecionar todos apenas na página
  atual`), cujo backlog registra bloqueio exclusivo pela paginação
  interativa do `ITEM-0003`.
- Fixa uma fronteira determinística entre página, foco, cursor lógico,
  seleção múltipla e filtro, evitando que a implementação futura precise
  inferir comportamento não decidido nas interseções entre essas quatro
  camadas de estado.
- Preserva integralmente a topologia toroidal por eixo dentro de uma página
  (ADR-0031) e a persistência da seleção entre páginas (ADR-0034), reduzindo
  o risco de regressão nas capacidades já entregues do `ITEM-0002` e do
  `ITEM-0006`.
- Declara explicitamente que D-PAG-10 não sobrescreve a reconciliação
  especializada por ID da ADR-0037, evitando ambiguidade de precedência no
  retorno pós-execução real do Handoff 4.

### Custos e restrições

- Exige que a implementação futura trate página como quarta camada de estado
  de runtime independente por console, além de foco, cursor e seleção já
  existentes, ampliando a superfície de estados a coordenar a cada evento
  (troca de página, retorno por foco, redimensionamento, mudança de modo,
  filtro, atualização de dados).
- Exige reconciliação determinística de cursor e página em pelo menos seis
  eventos distintos (D-PAG-02, D-PAG-05 a D-PAG-10), aumentando a superfície
  de casos de teste necessários antes da aceitação do futuro handoff.
- Introduz uma especialização por página da condição de existência do chip
  `[✥]` (D-PAG-04), que a implementação deverá recalcular a cada troca de
  página do console focado, não apenas a cada troca de foco entre consoles.
- Mantém em aberto, para decisão futura de aplicação e handoff, a
  representação concreta do estado de página, o algoritmo físico de quebra
  de páginas e o schema definitivo de `politica_paginacao` — o formato de
  objeto hoje presente em `config/telas/demo/demo.json` permanece rascunho e
  não é adotado por esta ADR.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `docs/contratos/contrato_console.md` | Registrar D-PAG-01 a D-PAG-13 como especialização da paginação já prevista em §12, e das seções 22 (navegação e foco, ADR-0031) e 23 (seleção múltipla e fluxo focal, ADR-0034/0037) quanto à interação com página. |
| `docs/contratos/contrato_barra_de_menus.md` | Registrar a topologia limitada de `[<][>]` (D-PAG-01), a especialização por página da condição de existência de `[✥]` (D-PAG-04) e a independência de página por console (D-PAG-13). |
| `docs/contratos/contrato_chip.md` | Registrar D-PAG-14 (entradas aceitas de `[<]`/`[>]`) e a distinção entre existência declarativa e ativação dinâmica dos controles de página por console (D-PAG-13). |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Avaliar necessidade de termos novos para topologia limitada de página, página sem item navegável e indicador `página 1/1` para conjunto vazio. |
| `docs/nomenclatura/32_CONSOLE.md` | Avaliar necessidade de termos novos para página como estado independente por console e para a interação entre página, filtro e reconciliação de cursor. |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Avaliar necessidade de registrar a especialização por página da condição de existência de `[✥]` (D-PAG-04). |
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0038 após QA favorável. |
| `docs/backlog.md` | Atualizar o estado do `ITEM-0003` quando o fluxo documental determinar mudança material; reavaliar o bloqueio do `ITEM-0018` à luz desta ADR. |

---

## 6. Compatibilidade e transição

Esta ADR não executa nenhuma aplicação documental, alteração de contrato,
alteração de nomenclatura, criação de handoff, implementação ou validação
manual — apenas registra a decisão fechada. Até a aplicação, os contratos e
módulos de nomenclatura listados na seção 5 permanecem no estado atual.

Console sem `politica_paginacao` declarada, ou com paginação de uma única
página implícita, preserva integralmente o comportamento histórico
(`contrato_console.md` §12); nenhuma migração automática de telas existentes
é introduzida por esta ADR. `config/telas/demo/demo.json` permanece
rascunho; nenhum schema de `politica_paginacao` é fixado por este documento
a partir dessa declaração antiga.

Esta ADR preserva integralmente:

- a topologia toroidal por eixo dentro de uma mesma página, o item lógico, o
  cursor, a lista de foco e os chips `[⇆]`/`[✥]` já fixados pela ADR-0031,
  exceto pela especialização pontual e explícita de D-PAG-04 sobre o
  universo de avaliação de `[✥]`;
- a identidade da seleção múltipla como conjunto de IDs estáveis, sua
  persistência entre páginas e o universo de `Todos` sobre o conjunto
  filtrado em todas as páginas, já fixados pela ADR-0034;
- o protocolo focal de execução sintética reversível da ADR-0035, a
  identidade e o carregamento da tela padrão de resultado da ADR-0036, e a
  integração do fluxo focal com `dry-run` e a reconciliação especializada
  por ID no retorno após execução real da ADR-0037 — nenhuma delas é
  reaberta ou redefinida; D-PAG-10 coexiste com a regra especializada da
  ADR-0037 sem sobrescrevê-la;
- a distinção entre existência declarativa (`regra_existencia`) e ativação
  dinâmica (`regra_ativo`) do chip, já fixada por `contrato_chip.md`;
- a distinção entre configuração concreta e estado de runtime já fixada por
  `docs/nomenclatura/01_NUCLEO_COMUM.md` — página permanece estado de
  runtime, não campo do `tela.json` como estado vivo.

---

## 7. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR. As decisões D-PAG-01 a
D-PAG-14 constituem decisão já fechada fornecida ao autor documental; este
documento não escolhe entre opções nem introduz arquitetura, schema ou
comportamento além do que foi explicitamente decidido.

---

## 8. Itens fora de escopo

- Representação concreta do estado de páginas em classes ou dicionários —
  decisão de implementação, não desta ADR.
- Nome definitivo de novos campos de runtime.
- Schema novo de `politica_paginacao` — o objeto hoje presente em
  `config/telas/demo/demo.json` permanece rascunho, não adotado por esta ADR.
- Algoritmo físico de quebra de páginas.
- Estrutura de buffers.
- APIs, classes, funções ou módulos.
- Desempenho, cache ou renderização parcial.
- Paginação multinível colapsável do `ITEM-0007`.
- Registry genérico de ações — `ITEM-0004`.
- Pilha genérica de telas — `ITEM-0005`.
- Persistência entre sessões.
- Alteração do protocolo focal das ADR-0034 a ADR-0037 — D-PAG-10 coexiste
  com a reconciliação especializada por ID da ADR-0037 sem alterá-la.
- Fixtures e roteiro de validação manual.
- Lista final de arquivos de implementação.
- QA da ADR, aplicação documental, atualização de índice ou de backlog,
  alteração de contrato ou de nomenclatura, criação de handoff,
  implementação, testes de implementação, stage e commit — fora desta
  execução.

---

## 9. Critérios para aplicação

- [x] `docs/contratos/contrato_console.md`, `docs/contratos/contrato_barra_de_menus.md`
  e `docs/contratos/contrato_chip.md` foram atualizados conforme a tabela de
  artefatos afetados (seção 5).
- [x] Somente os módulos proprietários da nomenclatura efetivamente afetados
  (`21`, `32`, `31`) foram avaliados e, quando material, atualizados.
- [x] `docs/adr/INDICE_ADR.md` foi atualizado somente após QA favorável desta
  ADR.
- [x] `docs/backlog.md` foi atualizado somente quando o fluxo documental
  determinar mudança material do `ITEM-0003` e do `ITEM-0018`.
- [x] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [x] Nenhum handoff foi criado na mesma etapa da aplicação documental.
- [x] Caminhos permanecem relativos à raiz do Orquestrador.
- [x] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [x] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [ ] A aplicação foi submetida a QA independente.

---

## 10. Relação com ADR-0031, ADR-0034 e ADR-0037

### 10.1 ADR-0031 — Navegação simples e seleção única em console de nível único

A ADR-0031 é preservada quanto a foco, cursor lógico, navegação toroidal por
eixo dentro de uma página, células vazias e proibição de as setas mudarem de
página (D8, D9, D15). Esta ADR não redefine nenhuma dessas regras.

É especializada pontualmente em dois pontos:

- **D-PAG-04** especializa a condição de existência do chip `[✥]` (ADR-0031
  D14): o universo de avaliação passa a ser a página atual do console
  focado, e não mais o console inteiro sem distinção de página — lacuna que
  a ADR-0031 deixava aberta por não tratar paginação.
- **D-PAG-05** especializa a regra de entrada sempre no item lógico `0`
  (ADR-0031 D6) para o caso de console paginado: ao retornar por foco, a
  página anterior do console é preservada e o cursor é reposicionado no
  primeiro item navegável dessa página preservada, não necessariamente no
  item lógico `0` absoluto do console inteiro.

O `ITEM-0003`, que a ADR-0031 declarava fora do seu escopo (D1, D15), passa a
ter suas próprias decisões fechadas por esta ADR.

### 10.2 ADR-0034 — Seleção múltipla e fluxo focal de processamento

A ADR-0034 é preservada quanto à seleção como conjunto de IDs estáveis
(D-SEL-01, D-SEL-02). A seleção continua persistindo entre páginas
(D-SEL-01, D-SEL-10); `Todos` continua abrangendo os itens selecionáveis do
conjunto filtrado em todas as páginas (D-SEL-06, D-SEL-10). Posição visual e
página não definem identidade da seleção (D-SEL-02) — esta ADR não altera
esse invariante: a topologia limitada (D-PAG-01), a troca de página
(D-PAG-02) e a repaginação (D-PAG-06 a D-PAG-10) atuam sobre cursor e página,
nunca sobre a identidade dos IDs selecionados.

Nenhuma decisão de D-SEL-01 a D-SEL-26 é reaberta por esta ADR.

### 10.3 ADR-0037 — Integração do fluxo focal com dry-run e restauração da origem

A ADR-0037 é preservada quanto à origem suspensa, ao retorno de `dry-run` e
ao retorno após execução real (D-H4-07 a D-H4-09). O retorno de `dry-run`
continua preservando página e cursor (D-H4-08) — esta ADR não altera essa
regra; a preservação de página em `dry-run` é caso particular já coberto
pela própria noção de origem suspensa como referência viva, não pela
repaginação genérica desta ADR. O retorno após execução real mantém sua
reconciliação especializada por ID (D-H4-09) — D-PAG-10 desta ADR é a regra
genérica de atualização dos dados para o `ITEM-0003` e não altera, não
sobrescreve e não é sobrescrita pela regra especializada da ADR-0037; as duas
regras operam em fronteiras distintas e coexistem sem contradição, conforme
declarado explicitamente em D-PAG-10.

Nenhuma decisão de D-H4-01 a D-H4-10 é reaberta por esta ADR.

### 10.4 Contratos vigentes

A topologia limitada já indicada para `[<]` e `[>]` em
`contrato_barra_de_menus.md` §8.3 (inativo na primeira/última página) é
preservada e detalhada por D-PAG-01. As especializações necessárias para
página atual, foco, cursor, chip `[✥]`, indicador e repaginação estão
explicitadas nas decisões D-PAG-01 a D-PAG-13 e na tabela de artefatos
afetados (seção 5). Esta ADR não aplica ainda essas alterações aos
contratos — a aplicação documental permanece para etapa distinta, sujeita a
QA favorável desta ADR.

---

## 11. Bloqueios

nenhum
