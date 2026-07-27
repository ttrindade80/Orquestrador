---
name: adr-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico
description: Formaliza regras operacionais de foco entre consoles navegáveis de nível único, cursor sobre item lógico, navegação toroidal por eixo, entrada sempre no item 0, preservação do item durante redistribuição, indicador derivado do estilo global e seleção única como item corrente
metadata:
  type: adr
  scope: navegacao_console_nivel_unico
  status: aceita
  data: "2026-07-25"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0002
  documentos_normativos_afetados_futuros:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_chip.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
---

# ADR-0031 — Navegação simples e seleção única em console de nível único

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0031 |
| Título | Navegação simples e seleção única em console de nível único |
| Status | aceita |
| Data | 2026-07-25 |
| Origem | Decisão explícita do usuário (2026-07-23 a 2026-07-24) |
| Item de backlog | ITEM-0002 |
| Levantamento 1 | `docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md` |
| Levantamento 2 | `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md` |

---

## 2. Status

`aceita`

```yaml
status_da_adr: aceita
qa_da_adr:
  resultado: ADR_QA_APPROVED_WITH_NOTES
  relatorio: docs/relatorios/RELATORIO_QA_ADR-0031.md
aplicacao_documental:
  executada: true
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
  qa_inicial: ADR_APPLICATION_QA_REJECTED
  patch_executado: true
  qa_pos_patch: ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES
handoff:
  id: H-0040
  criado: true
  estado_final_comprovado: H1_HANDOFF_APPROVED
implementacao:
  executada: true
  qa_final: I1_IMPLEMENTATION_APPROVED
validacao_manual:
  resultado: MANUAL_VALIDATION_APPROVED
consistencia_documental:
  resultado_atual: CONSISTENCIA_DOCUMENTAL_PATCH_REQUIRED
commit_do_ciclo: nao_executado
```

Esta ADR foi criada com status `ADR_CREATED_AWAITING_QA` a partir das decisões explícitas do usuário registradas no período 2026-07-23 a 2026-07-24 e dos levantamentos documentais realizados previamente. O QA semântico foi concluído com resultado `ADR_QA_APPROVED_WITH_NOTES` (relatório: `docs/relatorios/RELATORIO_QA_ADR-0031.md`). A ADR está semanticamente aprovada. A aplicação documental foi executada, teve QA inicial `ADR_APPLICATION_QA_REJECTED`, foi corrigida por patch e aprovada com notas em `ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES`. O handoff H-0040 foi criado e aprovado (`H1_HANDOFF_APPROVED`). A implementação foi executada e aprovada (`I1_IMPLEMENTATION_APPROVED`). A validação manual foi aprovada (`MANUAL_VALIDATION_APPROVED`). A consistência documental do ciclo encontra-se em correção (`CONSISTENCIA_DOCUMENTAL_PATCH_REQUIRED`); o commit do ciclo ainda não foi executado. Paginação, ações, seleção múltipla e navegação multinível permanecem deferidas conforme D15.

---

## 3. Contexto

### 3.1 Estado material ao início deste ciclo

O projeto acumulou, até o encerramento do Bloco 1 (ADR-0030 / H-0039), o seguinte conjunto de regras e capacidades vigentes relativas ao console:

**Já existiam:**

- Definição de `console` como container interativo e navegável (`docs/nomenclatura/32_CONSOLE.md`).
- Cursor sobre item lógico, não sobre linha física (`contrato_console.md` §7).
- Indicador `selecionado` → símbolo `→` materializado pelo estilo global (ADR-0030 D6).
- Estrutura do item com três partes: `ec` (espaço do cursor), `tg` (espaço de toggle) e `tx` (texto do item) (`docs/nomenclatura/32_CONSOLE.md` §4.4).
- Wrap toroidal como conceito: a grade fecha nos dois eixos independentemente; o cursor nunca entra em célula vazia; a paginação é independente da navegação (`docs/nomenclatura/32_CONSOLE.md` §4.3).
- Política de seleção única (`politica_selecao = "unica"`): cursor define o item alvo; sem toggle; `[␣]` não existe (`contrato_console.md` §8).
- Distinção entre foco entre elementos (`[⇆]`) e navegação dentro do console (`[✥]`) (`contrato_barra_de_menus.md` §8.3).
- Exclusão de `lancador` e `dashboard` de `[✥]` (ADR-0005; `contrato_console.md` §7).
- Regras de distribuição, matriz, redimensionamento, cardinalidade unitária e ocupação integral do corpo (ADR-0020 a ADR-0025).
- Apresentações multinível e modos verboso/não verboso (ADR-0026, ADR-0027, ADR-0028).
- Carregamento global e materialização do estilo (ADR-0030).

**Permaneciam ausentes ou incompletos:**

- Definição de quais consoles entram na lista de foco da tela.
- Definição de qual console recebe o foco inicialmente.
- Ordem de foco em grupos hierárquicos e assimétricos.
- Comportamento de Tab e Shift+Tab entre consoles.
- Item inicial de cada console ao receber foco.
- Algoritmo detalhado de movimento toroidal em linhas, colunas e matrizes incompletas.
- Preservação do item lógico corrente durante redistribuição ou mudança de modo.
- Condições concretas de exibição dos chips `[⇆]` e `[✥]` na navegação de consoles.
- Fronteira operacional entre seleção única (Bloco 2) e ações futuras (Blocos 3 e posteriores).

---

## 4. Problema

A ausência das regras listadas na seção 3.1 impedia a implementação de qualquer mecanismo de navegação e seleção única no console, mesmo que as regras de nível conceitual já estivessem presentes nos contratos e módulos de nomenclatura.

Em particular, não existia resposta para as seguintes questões operacionais:

1. Um console sem itens deve receber foco?
2. Um console declarado como navegável mas sem nenhum item navegável deve aparecer na lista de foco?
3. Ao entrar em um console, qual item recebe o cursor?
4. Ao retornar ao mesmo console por Tab, o cursor volta ao item anterior ou reinicia?
5. Em uma hierarquia de grupos com consoles aninhados de profundidade desigual, qual é a ordem do ciclo de Tab?
6. Em uma matriz com linhas incompletas, o que acontece ao pressionar ↓ em uma coluna sem item na linha seguinte?
7. O indicador `→` deve aparecer somente no console com foco ou em todos os consoles navegáveis?
8. A largura reservada para o indicador muda quando o cursor se move?
9. A barra de espaço e o indicador `●`/`○` pertencem a este ciclo?

Esta ADR responde essas questões por meio de 15 decisões operacionais (D1 a D15).

---

## 5. Escopo positivo

Este ciclo cobre exclusivamente:

- Foco entre consoles navegáveis de uma mesma tela.
- Navegação interna em console de nível único.
- Cursor sobre um item lógico.
- Seleção única como item corrente (item sob o cursor).
- Indicadores e chips necessários à navegação de consoles.
- Compatibilidade com redistribuição, redimensionamento e modos de apresentação.

---

## 6. Escopo negativo

Este ciclo exclui explicitamente:

- Paginação interativa (ITEM-0003).
- Registro e execução de ações (ITEM-0004).
- Abertura e retorno entre telas (ITEM-0005).
- Seleção múltipla (ITEM-0006).
- Navegação multinível e expansão/recolhimento (ITEM-0007).
- Conteúdo composto e heterogêneo (ITEM-0008).
- Dashboard passivo (ITEM-0009).

---

## 7. Autoridades consultadas

| Documento | Papel |
|---|---|
| `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md` | ADR antecedente; Bloco 1 concluído; `selecionado_simbolo` materializado |
| `docs/contratos/contrato_console.md` | Comportamento normativo do console, `politica_navegacao`, `navegavel` no item, seleção |
| `docs/contratos/contrato_barra_de_menus.md` | Chips `[⇆]` e `[✥]`, condições de existência e ativo/inativo |
| `docs/contratos/contrato_composicao_corpo.md` | Composição do corpo e grupos estruturais |
| `docs/contratos/contrato_json_console.md` | Envelope declarativo do conteúdo externo |
| `docs/contratos/contrato_tela_json.md` | JSON estrutural, políticas de tela |
| `docs/contratos/contrato_chip.md` | Classe chip, existência e ativo/inativo |
| `docs/nomenclatura/00_INDICE.md` | Roteador dos módulos de nomenclatura |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Terminologia de dimensões, paginação e redimensionamento |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Terminologia canônica de chips e barra de menus |
| `docs/nomenclatura/32_CONSOLE.md` | Terminologia de `ec`, `tg`, `tx`, cursor, wrap toroidal, navegação |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | Terminologia de apresentações multinível e modos |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md` | Inventário de decisões vigentes, lacunas e evidências |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md` | Compatibilidade com distribuição; invariantes de não regressão |

---

## 8. Genealogia das decisões

```yaml
decisoes_do_usuario:
  periodo: "2026-07-23 a 2026-07-24"
  abrange:
    - D1  (escopo do ciclo)
    - D2  (elegibilidade do console — critérios de focalização)
    - D3  (lista linear de foco por travessia em profundidade)
    - D4  (ordem espacial entre irmãos)
    - D5  (Tab e Shift+Tab circulares)
    - D6  (entrada sempre no item lógico 0)
    - D7  (ordem lógica dos itens em row-major)
    - D8  (navegação toroidal estrita por eixo)
    - D9  (casos degenerados e matriz incompleta)
    - D10 (preservação do item lógico durante redistribuição)
    - D11 (somente o console focado exibe o indicador)
    - D12 (reserva de coluna para o indicador)
    - D13 (seleção única como item sob cursor)
    - D14 (condições dos chips [⇆] e [✥])
    - D15 (paginação deferida; fronteira com ciclos futuros)

regras_contratuais_preexistentes:
  - cursor_navega_por_item_nao_linha_fisica         # contrato_console.md §7
  - politica_navegacao_como_campo_de_declaracao     # contrato_console.md §3 e §7
  - navegavel_como_campo_do_item                    # contrato_console.md §4
  - politica_selecao_unica_sem_toggle               # contrato_console.md §8
  - lancador_e_dashboard_excluidos_de_cursor        # ADR-0005; contrato_console.md §7
  - chip_setas_vinculado_a_console_navegavel        # contrato_barra_de_menus.md §11
  - chip_alternancia_alterna_foco_entre_elementos   # contrato_barra_de_menus.md §8.3
  - ec_tg_tx_partes_do_item                         # nomenclatura/32_CONSOLE.md §4.4
  - wrap_toroidal_e_paginacao_independente          # nomenclatura/32_CONSOLE.md §4.3
  - indicador_selecionado_preset_seta               # ADR-0030 D6
  - indicador_derivado_do_estilo_global             # ADR-0030 D8 e D10

evidencias_dos_levantamentos:
  - cursor_inicial_nao_confirmado_antes_deste_ciclo
  - foco_inicial_nao_confirmado_antes_deste_ciclo
  - ordem_exata_de_navegacao_nao_confirmada_antes_deste_ciclo
  - linha_incompleta_sem_regra_propria_antes_deste_ciclo
  - algoritmo_toroidal_parcialmente_definido_antes_deste_ciclo
  - preservacao_de_cursor_ao_redistribuir_nao_confirmada_antes_deste_ciclo

decisoes_tecnicas_de_handoff: []
```

### 8.1 Relação com o ciclo ADR-0030

- ADR-0030 concluiu o Bloco 1 (carregamento global e materialização do estilo).
- Os Blocos 2 (navegação e seleção única) e 3 (seleção múltipla) permaneceram futuros ao término de ADR-0030 e H-0039.
- Os levantamentos identificaram as lacunas operacionais ainda abertas no Bloco 2.
- O usuário fechou essas lacunas com as decisões D1 a D15 desta ADR.
- `ITEM-0002` registra a atividade correspondente no backlog.

---

## 9. Decisões — D1 a D15

### D1 — Escopo do ciclo

```yaml
escopo:
  inclui:
    - foco_entre_consoles_navegaveis
    - navegacao_interna_em_console_de_nivel_unico
    - cursor_sobre_um_item_logico
    - selecao_unica_como_item_corrente
    - indicadores_e_chips_necessarios_a_navegacao
    - compatibilidade_com_redimensionamento_e_modos

  exclui:
    - paginacao_interativa
    - registro_e_execucao_de_acoes
    - abertura_e_retorno_entre_telas
    - selecao_multipla
    - navegacao_multinivel
    - expansao_e_recolhimento
    - dashboard
```

Esta ADR não reabsorve itens que foram separados no backlog. Cada exclusão corresponde a um ITEM próprio (ITEM-0003 a ITEM-0009).

---

### D2 — Elegibilidade do console

Um console é **focalizável** quando satisfaz ambas as condições:

1. Declara navegação habilitada por meio do campo `politica_navegacao` da instância (`contrato_console.md` §3 e §7).
2. Possui ao menos um item com `navegavel: true` (`contrato_console.md` §4).

```yaml
console_focalizavel:
  requisitos:
    - declara_navegacao_habilitada_via_politica_navegacao
    - possui_ao_menos_um_item_com_navegavel_true

console_sem_declaracao_de_navegacao:
  entra_na_lista_de_foco: false

console_navegavel_sem_itens_com_navegavel_true:
  entra_na_lista_de_foco: false
  recebe_cursor: false
  exibe_indicador: false

dashboard:
  entra_na_lista_de_foco: false

lancador:
  entra_na_lista_de_foco: false
```

O mecanismo declarativo concreto é `politica_navegacao` (no console) e o campo `navegavel` (no item), ambos já definidos em `contrato_console.md`. Esta ADR não inventa campo ou schema novo.

---

### D3 — Lista linear de foco

A ordem de foco entre os consoles focalizáveis da tela é produzida por uma travessia hierárquica em profundidade da árvore de grupos e elementos do corpo.

```yaml
grupos_estruturais:
  recebem_foco: false

elementos_focalizaveis:
  tipo_neste_ciclo: CONSOLE_NAVEGAVEL_COM_ITENS

travessia:
  estrategia: PROFUNDIDADE_PRIMEIRO
  resultado: LISTA_LINEAR_ORDENADA
```

O resultado da travessia é uma lista linear de referências aos consoles focalizáveis, com um índice corrente indicando qual console está com o foco. Este modelo conceitual não impõe ponteiros literais, estrutura de dados específica ou arquitetura de implementação — essas escolhas pertencem ao handoff.

---

### D4 — Ordem espacial entre irmãos

Dentro de cada nível da travessia, a ordem de visita dos irmãos segue:

```yaml
ordem_entre_irmaos:
  horizontal: ESQUERDA_PARA_DIREITA
  vertical: CIMA_PARA_BAIXO
  matriz:
    dentro_da_linha: ESQUERDA_PARA_DIREITA
    entre_linhas: CIMA_PARA_BAIXO
  outras_composicoes: MAIS_ALTO_E_MAIS_A_ESQUERDA_PRIMEIRO
```

A quantidade desigual de descendentes entre grupos não altera a travessia: o visitador segue cada ramo até esgotar seus descendentes antes de avançar ao próximo irmão.

**Exemplo normativo de árvore assimétrica:**

```text
1
├── 1.1
│   ├── 1.1.1  [C] (console focalizável)
│   └── 1.1.2  [C] (console focalizável)
├── 1.2
│   ├── 1.2.1  [C] (console focalizável)
│   └── 1.2.2  [C] (console focalizável)
└── 1.3
    └── 1.3.1  [C] (console focalizável)

2
└── 2.1        [C] (console focalizável)
```

Ordem resultante da lista linear de foco:

```text
1.1.1
→ 1.1.2
→ 1.2.1
→ 1.2.2
→ 1.3.1
→ 2.1
```

---

### D5 — Tab e Shift+Tab

```yaml
Tab:
  sentido: DIRETO
  topologia: CIRCULAR
  ultimo_elemento: avanca_para_PRIMEIRO_ELEMENTO

Shift_Tab:
  sentido: INVERSO
  topologia: CIRCULAR
  primeiro_elemento: recua_para_ULTIMO_ELEMENTO
```

Tab e Shift+Tab percorrem exatamente a mesma lista linear produzida por D3/D4, em sentidos opostos. A topologia é circular: não há fim nem início absoluto da lista.

---

### D6 — Entrada em console

Sempre que o foco entra em um console focalizável — seja na primeira entrada, por Tab, por Shift+Tab, ou por retorno posterior ao mesmo console pela lista de foco —, o cursor é posicionado no item lógico `0`.

```yaml
cursor_destino: ITEM_LOGICO_0
restaurar_cursor_anterior_do_console: false
```

Não existe memória de cursor por console neste ciclo. O retorno ao mesmo console reinicia sempre no item `0`.

Esta regra vale para:

- Primeira entrada na tela.
- Entrada por Tab.
- Entrada por Shift+Tab.
- Retorno posterior ao mesmo console pela lista de foco.

---

### D7 — Ordem lógica dos itens

A posição lógica de cada item dentro do console segue a distribuição declarada:

```yaml
linha: ESQUERDA_PARA_DIREITA
coluna: CIMA_PARA_BAIXO
matriz: ROW_MAJOR
```

**Exemplo normativo:**

```text
00  01  02  03
04  05  06  07
08  09  10  11
```

O item lógico `0` é sempre o item `00`. A posição absoluta ocupada pelo conjunto no corpo não altera essa ordem. Linhas físicas produzidas pela quebra de conteúdo de um item não criam novos itens nem novas posições do cursor.

---

### D8 — Navegação toroidal por eixo

As setas navigam somente entre itens ocupados da página e da exibição atuais.

```yaml
esquerda_direita:
  dominio: MESMA_LINHA
  muda_de_linha: false
  topologia: TOROIDAL

cima_baixo:
  dominio: MESMA_COLUNA
  muda_de_coluna: false
  topologia: TOROIDAL

celulas_sem_item:
  recebem_cursor: false
  participam_do_toroide: false
```

Não existe:

- Salto diagonal.
- Busca pelo item geometricamente mais próximo.
- Mudança compensatória para outra linha quando ↔ atinge a borda.
- Mudança compensatória para outra coluna quando ↕ atinge a borda.
- Travessia sequencial linear pelas setas.
- Troca de página pelas setas.

---

### D9 — Casos degenerados e matriz incompleta

```yaml
um_item:
  quatro_setas: SEM_MOVIMENTO

uma_linha:
  esquerda_direita: TOROIDAL
  cima_baixo: SEM_MOVIMENTO

uma_coluna:
  cima_baixo: TOROIDAL
  esquerda_direita: SEM_MOVIMENTO
```

**Exemplo normativo de matriz incompleta:**

```text
00  01  02  03
04  05
```

Comportamento vertical (↕):

```text
00 ↕ 04    (coluna 0: toróide entre 00 e 04)
01 ↕ 05    (coluna 1: toróide entre 01 e 05)
02         (coluna 2: sem item na mesma coluna abaixo — SEM_MOVIMENTO vertical)
03         (coluna 3: sem item na mesma coluna abaixo — SEM_MOVIMENTO vertical)
```

Comportamento horizontal (↔):

```text
00 ↔ 01 ↔ 02 ↔ 03 ↔ (volta a 00)   (linha 0: toróide nos quatro itens)
04 ↔ 05 ↔ (volta a 04)               (linha 1: toróide nos dois itens)
```

As posições `(linha=1, coluna=2)` e `(linha=1, coluna=3)` não existem como posições do cursor. Elas não participam do toróide de nenhum eixo.

---

### D10 — Redistribuição e mudança de modo

Enquanto o console permanece focado, redistribuição ou mudança de modo preserva o item lógico corrente e recalcula os demais atributos visuais:

```yaml
preservar:
  - mesmo_item_logico

recalcular:
  - posicao_visual
  - linha_atual
  - coluna_atual
  - vizinhos_horizontais
  - vizinhos_verticais
  - distribuicao_fisica
```

A mudança entre modo verboso e não verboso segue a mesma regra. O redimensionamento ou a mudança de modo não reinicia o cursor no item `0`.

A regra de reinício no item `0` aplica-se à **entrada** no console (D6), não à redistribuição do console já focado.

---

### D11 — Console visualmente focado

Somente o console com foco atualmente exibe o indicador do item corrente.

```yaml
console_focado:
  exibe_indicador: true

outros_consoles:
  exibe_indicador: false

indicador_adicional_no_titulo:
  criar_neste_ciclo: false
```

Não se adiciona caractere extra ao título do console para indicar foco. O indicador visual é exclusivo da coluna `ec` do item corrente dentro do console focado.

---

### D12 — Coluna do indicador

Cada console navegável deve reservar uma coluna indicadora antes do conteúdo de cada item.

```yaml
item_corrente:
  primeira_linha_fisica: INDICADOR_SELECIONADO
  linhas_de_continuacao: ESPACO

demais_itens:
  primeira_linha_fisica: ESPACO
  linhas_de_continuacao: ESPACO
```

O indicador:

- Marca o início lógico do item.
- Não é repetido nas linhas de continuação do mesmo item.
- Não desloca o conteúdo quando o cursor muda de item — a coluna tem largura reservada de forma estável.
- Deve ser obtido do campo `selecionado_simbolo` do objeto de estilo global materializado (ADR-0030 D6 e D8), nunca hardcoded como `→` no renderizador.

O símbolo visual vigente é `→`, derivado do preset `"Seta"` definido pela ADR-0030. A referência ao símbolo concreto é ilustrativa nesta ADR; o renderizador deve consumir o campo do estilo, não o valor literal.

A reserva da coluna do indicador participa do cálculo de largura útil disponível para o conteúdo do item. Esse cálculo não viola as regras existentes de distribuição, ocupação, quebra, truncamento, matriz ou redimensionamento.

---

### D13 — Seleção única

Neste ciclo, seleção única significa:

```yaml
item_corrente:
  quantidade: UM
  identidade: ITEM_SOB_CURSOR
  persistencia_como_conjunto: false
  toggle_por_espaco: false
  indicador_de_inclusao: false
```

O item sob o cursor é o único alvo corrente do console. Não existe conjunto de itens selecionados neste ciclo.

A barra de espaço (`[␣]`) e os indicadores de inclusão (`tg` com `●`/`○`) pertencem ao ciclo de seleção múltipla (ITEM-0006, Bloco 3).

A execução de ação por Enter (`[⏎]`) não integra o escopo desta ADR. Contratos vigentes podem continuar registrando essa capacidade futura sem que esta ADR a implemente.

---

### D14 — Condições dos chips

```yaml
chip_alternancia:
  identificador_canonico: "[⇆]"
  aparece_quando: PELO_MENOS_DOIS_CONSOLES_FOCALIZAVEIS
  nao_aparece_com:
    - zero_consoles_focalizaveis
    - um_console_focalizavel

chip_setas:
  identificador_canonico: "[✥]"
  aparece_quando: CONSOLE_FOCADO_COM_MAIS_DE_UM_ITEM
  nao_aparece_com:
    - console_sem_itens_navegaveis
    - console_com_um_unico_item_navegavel
    - ausencia_de_console_focado
```

A condição considera consoles **focalizáveis** (D2), não apenas consoles declarados como navegáveis. Consoles navegáveis sem itens navegáveis não entram na contagem.

Não se inventa chip novo neste ciclo. Os identificadores `[⇆]` e `[✥]` são os canônicos vigentes dos contratos.

---

### D15 — Página atual e atividades deferidas

As setas permanecem restritas à página atual.

```yaml
setas_atravessam_paginas: false
```

A paginação interativa foi decidida em princípio, mas será implementada em ciclo separado (ITEM-0003):

```yaml
paginacao_interativa_futura:
  comandos:
    anterior: "<"
    proxima: ">"
  topologia: CICLICA
  cursor_na_pagina_destino: ITEM_0
  ciclo: ITEM-0003
```

Essa regra aparece como **fronteira de compatibilidade**: a implementação futura de ITEM-0003 não deve entrar em conflito com as regras estabelecidas em D6 a D10.

**Atividades deferidas:**

| ITEM | Descrição |
|---|---|
| ITEM-0003 | Paginação interativa do console |
| ITEM-0004 | Registro e execução declarativa de ações individuais |
| ITEM-0005 | Abertura e retorno entre telas por ação |
| ITEM-0006 | Seleção múltipla no console |
| ITEM-0007 | Conteúdo multinível colapsável no console |
| ITEM-0008 | Conteúdo composto e heterogêneo no console |
| ITEM-0009 | Dashboard passivo de resumo |

---

## 10. Modelo conceitual

A lista de foco pode ser compreendida conceitualmente como:

```text
lista_de_foco  = [console_A, console_B, console_C, ...]
indice_corrente = 0   → console_A tem o foco
```

Tab incrementa o índice (com wraparound). Shift+Tab decrementa (com wraparound). A entrada em qualquer console sempre posiciona o cursor no item lógico `0` desse console.

Dentro de cada console focado, o estado de navegação pode ser concebido como:

```text
item_corrente = 0   (índice lógico na página atual)
```

As setas atualizam `item_corrente` segundo as regras de D8/D9. Redistribuição ou mudança de modo recalcula a posição visual a partir de `item_corrente` sem alterá-lo (D10).

Este modelo é conceitual. Não prescreve nome de variável, classe, módulo ou estrutura de dados. O handoff de implementação escolherá a representação concreta.

---

## 11. Exemplos normativos

Os exemplos normativos estão incorporados nas decisões D4 e D9. Esta seção consolida as referências.

### 11.1 Travessia em profundidade (D4)

```text
1                   (grupo estrutural — não focalizável)
├── 1.1             (grupo estrutural — não focalizável)
│   ├── 1.1.1  [C] (console focalizável)
│   └── 1.1.2  [C] (console focalizável)
├── 1.2             (grupo estrutural — não focalizável)
│   ├── 1.2.1  [C] (console focalizável)
│   └── 1.2.2  [C] (console focalizável)
└── 1.3             (grupo estrutural — não focalizável)
    └── 1.3.1  [C] (console focalizável)

2                   (grupo estrutural — não focalizável)
└── 2.1        [C] (console focalizável)

Ordem da lista de foco:
1.1.1 → 1.1.2 → 1.2.1 → 1.2.2 → 1.3.1 → 2.1
```

### 11.2 Matriz incompleta (D9)

```text
Distribuição dos itens:
00  01  02  03
04  05

Movimento ↔ (horizontal):
  Linha 0: 00 ↔ 01 ↔ 02 ↔ 03 ↔ (volta a 00)
  Linha 1: 04 ↔ 05 ↔ (volta a 04)

Movimento ↕ (vertical):
  Coluna 0: 00 ↕ 04 ↕ (volta a 00)
  Coluna 1: 01 ↕ 05 ↕ (volta a 01)
  Coluna 2: 02 permanece em 02
  Coluna 3: 03 permanece em 03
```

---

## 12. Alternativas rejeitadas

### A1 — Tornar todos os consoles navegáveis por padrão

**Rejeitada.** Console sem declaração de navegação pode ser um componente passivo de exibição. Torná-lo navegável por padrão violaria o princípio declarativo do sistema (ADR-0008) e incluiria na lista de foco elementos que o autor da tela não pretendia navegar.

### A2 — Permitir foco em console sem itens navegáveis

**Rejeitada.** Um console sem itens navegáveis não tem destino para o cursor. Incluí-lo na lista de foco criaria uma entrada inútil e comportamento indefinido ao tentar posicionar o cursor.

### A3 — Atribuir foco a grupos estruturais

**Rejeitada.** Grupos são elementos de composição, não de interação. A navegação ocorre entre consoles, que são os containers interativos. Focar em grupos introduziria uma camada intermediária sem valor funcional e incompatível com a distinção já estabelecida entre elementos de corpo e contêineres estruturais.

### A4 — Ordenar o foco apenas pela quantidade de elementos

**Rejeitada.** A contagem de descendentes não reflete a posição visual na tela. Uma ordenação por quantidade quebraria a intuição espacial do usuário, que espera que Tab mova o foco de forma consistente com a disposição visual dos elementos.

### A5 — Procurar o elemento geometricamente mais próximo

**Rejeitada.** A busca pelo vizinho mais próximo em geometria 2D é algoritmicamente cara e ambígua em casos de equidistância. A travessia em profundidade é determinística, previsível e independente da distribuição física calculada pelo renderer.

### A6 — Navegar pelas setas em uma sequência linear global

**Rejeitada.** As setas têm semântica de eixo: ↔ é horizontal, ↕ é vertical. Transformar as quatro setas em sequência linear global confunde o modelo mental do usuário e torna o comportamento dependente de uma ordem de serialização arbitrária.

### A7 — Permitir que esquerda/direita troquem de linha

**Rejeitada.** Esquerda/direita têm domínio na mesma linha. Permitir troca de linha transforma o comportamento em uma travessia linear disfarçada de navegação 2D e produziria saltos não intuitivos em matrizes grandes.

### A8 — Permitir que cima/baixo troquem de coluna

**Rejeitada.** Pelo mesmo motivo de A7. Cima/baixo têm domínio na mesma coluna. A troca de coluna quebraria a semântica de eixo vertical.

### A9 — Atravessar páginas pelas setas

**Rejeitada.** Cada página é um toróide fechado. Cruzar páginas pelas setas sem controle explícito tornaria o comportamento imprevisível. A paginação interativa será tratada em ITEM-0003 com comandos específicos (`<` e `>`).

### A10 — Restaurar o item anteriormente focado ao retornar a um console

**Rejeitada.** Manter memória de cursor por console requer estado adicional e cria comportamento de difícil explicação ao usuário. A regra uniforme de reinício em `0` é simples, previsível e consistente com o modelo de entrada.

### A11 — Reiniciar o cursor após redistribuição ou mudança de modo

**Rejeitada.** Reiniciar o cursor ao redistribuir quebraria a continuidade da interação. Se o usuário está no item `07` e redimensiona o terminal, espera que o cursor continue no item `07`, mesmo que sua posição visual mude. A preservação do item lógico é coerente com o modelo de item como entidade estável.

### A12 — Exibir o indicador em todos os consoles navegáveis simultaneamente

**Rejeitada.** O indicador comunica "este é o item sobre o qual a próxima ação atuará". Exibi-lo em múltiplos consoles ao mesmo tempo cria ambiguidade sobre qual console e qual item são o alvo atual.

### A13 — Colocar o indicador em todas as linhas físicas do item

**Rejeitada.** O indicador marca o início lógico do item, não cada linha física. Repetir o indicador nas linhas de continuação confundiria o usuário e quebraria a distinção entre primeira linha física e linhas de continuação já presente nos modos verboso e não verboso.

### A14 — Alterar a largura útil quando o indicador muda de posição

**Rejeitada.** A largura da coluna do indicador é fixa. Alterar a largura útil a cada mudança de cursor causaria redistribuição visual a cada tecla pressionada — comportamento inaceitável por desempenho e experiência do usuário.

### A15 — Unir paginação, ações, seleção múltipla ou navegação multinível ao mesmo ciclo

**Rejeitada.** Cada capacidade tem dependências, estados e contratos próprios. Unir múltiplos ciclos dificulta revisão, QA e rastreabilidade. O backlog já separou essas capacidades em ITEMs independentes (ITEM-0003 a ITEM-0009).

### A16 — Impor ponteiros literais ou uma estrutura de implementação específica

**Rejeitada.** A ADR define regras operacionais, não código. Prescrever ponteiros, tipos de dados ou arquitetura de módulo prematuramente limita as opções de implementação e pode tornar a ADR tecnicamente obsoleta antes de ser aplicada.

---

## 13. Consequências

### 13.1 Necessidades de estado em runtime

- **Estado de foco de tela**: a tela precisa saber qual console está com o foco atualmente.
- **Coleção linear ordenada de consoles focalizáveis**: resultado da travessia D3/D4, mantido em runtime.
- **Posição corrente na coleção**: índice que aponta para o console focado.
- **Item corrente no console focado**: posição lógica do cursor dentro do console com foco.

### 13.2 Ausências intencionais

- **Sem memória de cursor por console durante troca de foco**: ao retornar ao mesmo console, o cursor recomeça do item `0` (D6).
- **Sem memória de item entre sessões**: estado de runtime não é persistido.

### 13.3 Necessidades de cálculo

- **Recálculo de vizinhanças após redistribuição**: mudança de modo ou redimensionamento altera quais itens estão à esquerda, direita, cima e baixo do item corrente (D10).
- **Separação entre item lógico e linha física**: a mesma posição lógica pode ocupar diferentes linhas físicas conforme o modo (D12).
- **Reserva de espaço para o indicador**: a coluna `ec` deve ser reservada antes do conteúdo do item, participando do cálculo de largura útil.

### 13.4 Dependência do estilo global

O símbolo do indicador deve ser obtido do campo `selecionado_simbolo` do objeto de estilo global materializado (ADR-0030). Qualquer mudança de preset de estilo reflete automaticamente no indicador de cursor.

### 13.5 Necessidades de teste

- Testes com árvores de grupos assimétricas (D4).
- Testes com consoles em linhas e colunas unitárias (D9).
- Testes com matrizes incompletas (D9).
- Testes de preservação do item lógico após redistribuição (D10).
- Testes de preservação do item lógico após mudança de modo (D10).

### 13.6 Não regressão

As regras de distribuição e redimensionamento já implementadas devem ser preservadas sem alteração. O cursor é uma camada sobreposta à distribuição — não a redefine.

---

## 14. Compatibilidade e não regressão

### 14.1 Matriz de ADRs preservadas

| ADR | Assunto | Relação com esta ADR |
|---|---|---|
| ADR-0020 | Matriz de grupos e coordenadas explícitas | Grupos estruturais não recebem foco; coordenadas declaradas permanecem vigentes; o cursor navega sobre itens dos consoles, não sobre posições do grupo |
| ADR-0024 | Proibição de preenchimento vazio externo do corpo | Ocupação integral do corpo preservada; a reserva da coluna do indicador é interna ao console, não externa ao corpo |
| ADR-0025 | Distribuição matricial configurável de nível único | A distribuição não é alterada; o cursor é sobreposto à distribuição existente; a reserva do indicador respeita as regras de largura |
| ADR-0026 | Fornecimento externo de dados ao console | Conteúdo externo permanece separado do JSON estrutural; o cursor navega sobre os itens do conteúdo externo já carregado |
| ADR-0027 | Carregamento conjunto da tela e do conteúdo externo | Fluxo de carregamento não é alterado por esta ADR |
| ADR-0028 | Apresentações de conteúdo multinível e alternância verbosa | Modos verboso/não verboso preservados; mudança de modo preserva o item lógico corrente (D10) |
| ADR-0030 | Carregamento global e materialização do estilo | O indicador é obtido do estilo materializado; `→` não é hardcoded no renderizador |

### 14.2 Invariantes de distribuição e layout preservadas

- Distribuição horizontal, vertical e matricial vigente.
- Ordem visual calculada pelo layout.
- Ocupação integral do corpo (ADR-0024).
- Responsividade ao redimensionamento (ADR-0017).
- Cardinalidade unitária (ADR-0024).
- Linhas incompletas na distribuição.
- Conteúdo externo (ADR-0026, ADR-0027).
- Apresentações multinível existentes (ADR-0028).
- Modo verboso e não verboso (ADR-0028).
- Redimensionamento livre (ADR-0017).
- Paginação já existente como apresentação (`contrato_console.md` §12).
- Separação entre configuração estrutural e estado de runtime.

### 14.3 Terminologia preservada

- `ec`, `tg` e `tx` permanecem como terminologia vigente do domínio de console (`docs/nomenclatura/32_CONSOLE.md`).
- Esta ADR não infere materialização física obrigatória de `ec`, `tg` e `tx` como colunas de largura fixa para todas as apresentações.
- Esta ADR define que `ec` reserva uma coluna para o indicador; não impõe que essa reserva constitua uma coluna geométrica independente com largura própria fora da unidade do item.

### 14.4 Ausências de navegação preservadas

- `dashboard` não entra na lista de foco (ADR-0005; `contrato_console.md` §15).
- `lancador` não entra na lista de foco (ADR-0005; `contrato_barra_de_menus.md` §11).

### 14.5 Limites desta ADR

Esta ADR não redefine geometria, distribuição, schema ou comportamento de elementos fora das decisões D1 a D15. Qualquer extensão de escopo requer nova ADR.

---

## 15. Aplicação futura

Esta ADR deve ser aplicada nos documentos abaixo, na ordem indicada pelo fluxo documental vigente. **Nenhum desses documentos é alterado neste passo.**

| Documento | Classificação | Observação |
|---|---|---|
| `docs/contratos/contrato_console.md` | ATUALIZAR | Registrar D2, D6, D7, D10, D12, D13; revisar condições de navegação e coluna do indicador |
| `docs/contratos/contrato_barra_de_menus.md` | ATUALIZAR | Registrar D14; refinar condições de `[⇆]` (mínimo 2 consoles focalizáveis) e `[✥]` (console focado com mais de um item) |
| `docs/contratos/contrato_chip.md` | ATUALIZAR_SE_AFETADO | Verificar se condições de existência dos chips canônicos precisam de ajuste |
| `docs/contratos/contrato_composicao_corpo.md` | ATUALIZAR_SE_AFETADO | Verificar compatibilidade com D3/D4 (lista de foco por travessia) |
| `docs/contratos/contrato_json_console.md` | INSPECIONAR_E_PRESERVAR | Envelope declarativo não muda; verificar compatibilidade |
| `docs/contratos/contrato_tela_json.md` | INSPECIONAR_E_PRESERVAR | Verificar se o JSON estrutural precisa de campo para suportar as políticas declaradas; não alterar sem decisão específica |
| `docs/nomenclatura/32_CONSOLE.md` | ATUALIZAR_SE_AFETADO | Verificar se D3–D13 requerem termos adicionais na nomenclatura do console |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | ATUALIZAR_SE_AFETADO | Verificar se D14 requer ajuste na terminologia dos chips |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | PRESERVAR | Separação entre paginação e navegação preservada; D15 não altera este módulo |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | INSPECIONAR_E_PRESERVAR | Verificar compatibilidade com D10 |
| `docs/adr/INDICE_ADR.md` | ATUALIZAR | Somente após QA favorável desta ADR |
| `docs/backlog.md` | PRESERVAR | Somente quando o fluxo documental determinar mudança real do estado do ITEM-0002 |

**Regras de aplicação:**

- `docs/adr/INDICE_ADR.md` só é atualizado após QA favorável desta ADR.
- `docs/backlog.md` só é atualizado quando o fluxo documental determinar mudança real do estado do ITEM-0002.
- Documentos de paginação preservam apenas a separação do ciclo futuro (ITEM-0003).
- Contratos de ações não devem ser completados por esta ADR.

---

## 16. Validações arquiteturais futuras

Os critérios abaixo deverão ser materializados em contrato, handoff e testes:

1. Tela sem console focalizável: nenhum foco é estabelecido; `[⇆]` e `[✥]` ausentes ou inativos.
2. Console navegável com um item: `[✥]` inativo; setas sem movimento.
3. Console navegável com vários itens em linha: `[✥]` ativo; ↔ toroidal na linha; ↕ sem movimento.
4. Console navegável com vários itens em coluna: `[✥]` ativo; ↕ toroidal na coluna; ↔ sem movimento.
5. Matriz completa: `[✥]` ativo; ↔ toroidal por linha; ↕ toroidal por coluna.
6. Matriz com última linha incompleta: comportamento conforme D9; células vazias sem cursor.
7. Dois consoles navegáveis lado a lado: `[⇆]` ativo; Tab/Shift+Tab circulares entre os dois.
8. Grupos aninhados e assimétricos: ordem de Tab conforme D4 (profundidade-primeiro, esquerda para direita).
9. Tab circular: do último console volta ao primeiro.
10. Shift+Tab circular: do primeiro console volta ao último.
11. Retorno a console reiniciando no item `0`: ao pressionar Tab voltando ao mesmo console, cursor em `0`.
12. Console navegável sem itens navegáveis fora da lista: não recebe foco, não exibe indicador.
13. Console não navegável fora da lista: não recebe foco.
14. Somente o console focado exibindo o indicador: demais consoles sem símbolo na coluna `ec`.
15. Linhas físicas de continuação sem repetir o indicador: somente a primeira linha física do item corrente exibe o símbolo.
16. Reserva estável da coluna do indicador: a largura reservada não muda quando o cursor muda de item.
17. Redimensionamento preservando o item lógico: após SIGWINCH, o cursor continua no mesmo item lógico.
18. Troca de modo preservando o item lógico: ao pressionar V, o cursor continua no mesmo item lógico.
19. Recálculo da navegação após redistribuição: os vizinhos do item corrente são recalculados com a nova distribuição.
20. Chips ausentes quando não produzem movimento: `[✥]` inativo ou ausente quando console tem único item.
21. Setas sem atravessar páginas: ↔↕ ficam no toróide da página atual.
22. Ausência de comportamento de seleção múltipla: `[␣]` não existe neste ciclo.
23. Ausência de execução de ações neste ciclo: `[⏎]` não executa ação de item dentro do escopo desta ADR.

---

## 17. Decisões deferidas

| Decisão deferida | Item de backlog | Razão |
|---|---|---|
| Paginação interativa (`<` e `>`) | ITEM-0003 | Ciclo separado; regras próprias de cursor na página destino |
| Registro e execução declarativa de ações | ITEM-0004 | Depende de DOC-B009; ciclo separado |
| Abertura e retorno entre telas | ITEM-0005 | Depende de ações formalizadas; ciclo separado |
| Seleção múltipla (`[␣]`, `●`/`○`) | ITEM-0006 | Bloco 3; ciclo separado |
| Conteúdo multinível colapsável | ITEM-0007 | Ciclo separado |
| Conteúdo composto e heterogêneo | ITEM-0008 | Ciclo separado |
| Dashboard passivo | ITEM-0009 | Ciclo separado |
| Memória de cursor por console entre entradas | — | Alternativa A10 rejeitada neste ciclo; reconsideração requer nova ADR |
| Símbolo estático de `tg` em item navegável sem seleção real | — | Deferido da ADR-0030 D12; depende de decisão futura |
| Registry completo de ações (DOC-B009) | ITEM-0004 | Identificado nos levantamentos; arquivo próprio não encontrado |

---

## 18. Rastreabilidade

### 18.1 Origem das decisões

| Decisão | Origem | Referência |
|---|---|---|
| D1 | Usuário | Escopo explícito do ciclo |
| D2 | Usuário + regra contratual preexistente | `contrato_console.md` §3, §4, §7 |
| D3 | Usuário | Travessia em profundidade como mecanismo de ordenação |
| D4 | Usuário | Ordem espacial entre irmãos |
| D5 | Usuário | Tab/Shift+Tab circulares |
| D6 | Usuário | Entrada sempre no item 0 |
| D7 | Usuário | Ordem lógica row-major |
| D8 | Usuário | Navegação toroidal estrita por eixo |
| D9 | Usuário | Casos degenerados e matriz incompleta |
| D10 | Usuário | Preservação do item lógico durante redistribuição |
| D11 | Usuário | Exclusividade do indicador ao console focado |
| D12 | Usuário + regra contratual preexistente | `ec` em `nomenclatura/32_CONSOLE.md`; `selecionado_simbolo` em ADR-0030 D6 |
| D13 | Usuário + regra contratual preexistente | `contrato_console.md` §8; ADR-0030 D13 |
| D14 | Usuário | Condições refinadas dos chips |
| D15 | Usuário | Fronteira com paginação interativa e demais ciclos |

### 18.2 Separação genealógica

```yaml
decisoes_do_usuario:
  - D1  (escopo do ciclo)
  - D2  (critérios de focalização — regra sobre quais consoles entram)
  - D3  (travessia em profundidade)
  - D4  (ordem espacial entre irmãos)
  - D5  (Tab/Shift+Tab circulares)
  - D6  (entrada no item 0)
  - D7  (ordem lógica row-major)
  - D8  (navegação toroidal estrita por eixo)
  - D9  (casos degenerados)
  - D10 (preservação do item lógico)
  - D11 (exclusividade do indicador)
  - D12 (reserva de coluna para indicador)
  - D13 (seleção única sem toggle)
  - D14 (condições dos chips)
  - D15 (fronteira com ciclos futuros)

regras_contratuais_preexistentes:
  - navegavel_em_itens         # contrato_console.md §4
  - politica_navegacao         # contrato_console.md §3
  - selecao_unica_sem_toggle   # contrato_console.md §8
  - lancador_excluido          # ADR-0005
  - dashboard_excluido         # contrato_console.md §15
  - ec_tg_tx                   # nomenclatura/32_CONSOLE.md
  - selecionado_simbolo        # ADR-0030 D6

evidencias_dos_levantamentos:
  - lacunas_operacionais_identificadas     # RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md §25
  - invariantes_de_nao_regressao           # RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md §11
  - cursor_inicial_nao_confirmado_antes    # RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md §21
  - foco_inicial_nao_confirmado_antes      # RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md §21

decisoes_tecnicas_de_handoff: []
```

### 18.3 Relação com os levantamentos

Os levantamentos foram tratados como evidência e inventário, não como fonte de decisão:

- `RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md`: identificou 20 dimensões abertas; nenhuma dimensão foi promovida automaticamente a decisão por este levantamento — o fechamento veio das decisões explícitas do usuário.
- `RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md`: registrou invariantes de não regressão; confirmou que `ec`, `tg` e `tx` são terminologia ativa sem materialização física comprovada; confirmou que a ordem de navegação era `NAO_CONFIRMADA` antes deste ciclo.

Os levantamentos não prevalecem sobre as decisões D1 a D15. Onde há divergência entre o levantamento e uma decisão do usuário, prevalece a decisão.

---

## 19. Matriz de propagação documental

| Arquivo | Classificação | Observação |
|---|---|---|
| `docs/contratos/contrato_console.md` | ATUALIZAR | Registrar D2, D6, D7, D10, D12, D13 |
| `docs/contratos/contrato_barra_de_menus.md` | ATUALIZAR | Registrar D14; refinar condições de `[⇆]` e `[✥]` |
| `docs/contratos/contrato_composicao_corpo.md` | ATUALIZAR_SE_AFETADO | Verificar compatibilidade com D3/D4 |
| `docs/contratos/contrato_json_console.md` | INSPECIONAR_E_PRESERVAR | Envelope declarativo não muda |
| `docs/contratos/contrato_tela_json.md` | INSPECIONAR_E_PRESERVAR | Verificar suporte às políticas declaradas |
| `docs/contratos/contrato_chip.md` | ATUALIZAR_SE_AFETADO | Verificar condições de existência dos chips |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | PRESERVAR | Separação paginação/navegação preservada |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | ATUALIZAR_SE_AFETADO | Verificar D14 na terminologia dos chips |
| `docs/nomenclatura/32_CONSOLE.md` | ATUALIZAR_SE_AFETADO | Verificar D3–D13 na nomenclatura do console |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | INSPECIONAR_E_PRESERVAR | Verificar compatibilidade com D10 |
| `docs/adr/INDICE_ADR.md` | ATUALIZAR | Somente após QA favorável desta ADR |
| `docs/backlog.md` | PRESERVAR | Somente quando o fluxo documental determinar mudança real do estado do ITEM-0002 |

---

## 20. Encerramento

```yaml
status_da_adr: aceita
status_anterior_criacao: ADR_CREATED_AWAITING_QA
qa_da_adr:
  resultado: ADR_QA_APPROVED_WITH_NOTES
  relatorio: docs/relatorios/RELATORIO_QA_ADR-0031.md
aplicacao_documental:
  executada: true
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
  qa_inicial: ADR_APPLICATION_QA_REJECTED
  patch_executado: true
  qa_pos_patch: ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES
handoff:
  id: H-0040
  criado: true
  estado_final_comprovado: H1_HANDOFF_APPROVED
implementacao:
  executada: true
  qa_final: I1_IMPLEMENTATION_APPROVED
validacao_manual:
  resultado: MANUAL_VALIDATION_APPROVED
consistencia_documental:
  resultado_atual: CONSISTENCIA_DOCUMENTAL_PATCH_REQUIRED
decisoes_propagadas:
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
arquivo_criado: docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
item_de_backlog: ITEM-0002
commit_executado: nao
```

ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES
