---
name: ADR-0042-navegacao-multinivel-do-console
description: "Fecha as políticas de navegação multinível do console (nivel_unico preservado, tabela passiva, arvore_colapsavel, selecao_multinivel, dois_niveis_por_foco), sua declaração discriminada em politica_navegacao, a semântica de Espaço associada a cada política, a seleção exclusiva obrigatória de filho por pai em dois_niveis_por_foco, a derivação binária de seleção e reconciliação hierárquica de selecao_multinivel, a coerência estrutural de selecionabilidade, a subordinação integral à paginação universal da ADR-0041 e o isolamento em relação à tentativa multinível anterior preservada em branch de erro"
metadata:
  type: adr
  status: aceita
  id: ADR-0042
  data: "2026-08-08"
  substitui: null
rastreabilidade:
  decisao_usuario: "D-MULTI-01 a D-MULTI-13 — escopo do ciclo restrito a navegação multinível do console (políticas explícitas de navegação, foco entre consoles, cursor dentro do console, nivel_unico, tabela, arvore_colapsavel, selecao_multinivel, dois_niveis_por_foco, semântica de Espaço associada, integração com a apresentação de seleção já existente); regras transversais de foco/cursor/política declarada; preservação de nivel_unico; tabela como apresentação passiva sem cursor; arvore_colapsavel como hierarquia navegável sem seleção; selecao_multinivel como topologia única de profundidade arbitrária com Espaço recursivo; dois_niveis_por_foco com toroide de pais, toroide de filhos por pai e escolha exclusiva obrigatória de filho por pai; declaração de politica_navegacao como objeto com discriminador tipo e valores fechados; fallback de tipo ausente para nivel_unico para compatibilidade; subordinação integral da paginação à ADR-0041; isolamento explícito da tentativa multinível anterior preservada em branch de erro; D-MULTI-06-P03 — estado selecionado derivado e propagação bidirecional na hierarquia; D-MULTI-07-P04 — coerência estrutural de selecionabilidade"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0007
  contratos_afetados:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
  handoffs_bloqueados: []
---

# ADR-0042 — Navegação multinível do console

## 1. Status

`aceita`

```yaml
status_da_adr: aceita
qa_da_adr:
  resultado: ADR_APPROVED
  relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0042_P04.md
patch:
  aplicado: true
  id: P04
  relatorio: docs/relatorios/RELATORIO_PATCH_ADR-0042_P04.md
aplicacao_documental:
  executada: true
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0042_P04.md
  qa_da_aplicacao: ADR_APPLICATION_APPROVED
  qa_relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0042_P04.md
handoff:
  id: H-0052
  qa: H1_HANDOFF_APPROVED
  relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0052_P01.md
implementacao:
  status: IMPLEMENTED
  relatorio: docs/relatorios/IMP-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
  qa: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0052_P08.md
validacao_manual:
  status: MANUAL_VALIDATION_APPROVED
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0052.md
```

Esta ADR foi criada a partir de treze decisões fechadas fornecidas ao autor
documental (D-MULTI-01 a D-MULTI-13). Nenhuma delas foi escolhida, reaberta
ou alterada por este documento. Não há arquitetura, schema, política,
representação visual ou fluxo de execução introduzido além do que foi
explicitamente decidido. Aplicação documental, handoff, implementação e
validação manual são etapas posteriores, fora desta execução.

---

## 2. Contexto

### 2.1 Estado material ao início deste ciclo

O `docs/backlog.md` registra o `ITEM-0007` — navegação multinível do console
— como item planejado, com pré-requisito o ciclo universal de paginação por
`PageUp`/`PageDown` e chips `[PgUp][PgDn]`, concluído pela ADR-0041 e pelo
`H-0051`, com QA técnico e validação manual aprovados. O próprio backlog
registra que o ciclo do `ITEM-0007` **não pode reaproveitar a tentativa
defeituosa preservada em branch de erro**.

A ADR-0031 fechou navegação simples e seleção única para console de nível
único (foco entre consoles, cursor por item lógico, navegação toroidal por
eixo, indicador de item corrente). A ADR-0034 fechou seleção múltipla e
fluxo focal de processamento (conjunto de IDs estáveis, reconciliação,
apresentação por `tg` com `●`/`○`). A ADR-0038 fechou a paginação
interativa limitada do console, com tecla e representação visual
posteriormente especializadas pela ADR-0041 para `PageUp`/`PageDown` e
`[PgUp][PgDn]`, de forma universal e vinculante para toda paginação
presente ou futura do Orquestrador — inclusive a deste ciclo (D-PGU-08).

O `contrato_console.md` (§19–§21) e o `contrato_json_console.md` (§11–§13)
já fixam a fronteira declarativa do conteúdo multinível externo — schema
semântico, tipos de nível (`container`, `conteudo`, `nome_valor`),
apresentações (`tabela`, `hierarquia`, `conjuntos_campos`) e alternância
verboso/não verboso — sem fechar navegação, seleção, expansão ou
recolhimento de níveis. O módulo `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_
CONSOLE.md` registra explicitamente, em sua seção 8B, que "navegação
multinível está fora da ADR-0031" e que "colapsamento, expansão e travessia
entre níveis pertencem ao `ITEM-0007`".

### 2.2 Problema

Sem esta ADR, não existe autoridade documental fechada para o cursor, o
percurso e a semântica de Espaço aplicáveis a conteúdo multinível do
console. As capacidades `arvore_colapsavel`, `selecao_multinivel` e
`dois_niveis_por_foco` não possuem definição comportamental alguma; a
apresentação `tabela`, hoje passiva conforme os contratos vigentes, não
possui declaração explícita de sua não navegabilidade; e `nivel_unico` não
possui remissão explícita de que seu comportamento vigente (ADR-0031,
ADR-0034, ADR-0038/0041) é preservado sem redesenho no contexto multinível.
Esta ADR responde a essa lacuna por meio de treze decisões fechadas
(D-MULTI-01 a D-MULTI-13), restritas ao escopo declarado, sem introduzir
arquitetura, schema, política, representação visual ou fluxo de execução
além do que foi explicitamente fechado.

### 2.3 Autoridades consultadas

| Documento | Papel |
|---|---|
| `docs/backlog.md` | Registra o `ITEM-0007`, seu pré-requisito satisfeito pela ADR-0041 e a proibição de reaproveitar a tentativa preservada em branch de erro |
| `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md` | Autoridade universal de paginação (`PageUp`/`PageDown`, `[PgUp][PgDn]`), vinculante para esta ADR por D-PGU-08 |
| `docs/contratos/contrato_console.md` | Autoridade comportamental vigente do console — foco (§22, ADR-0031), seleção múltipla (§23, ADR-0034), paginação (§24, ADR-0038/ADR-0041) e apresentação de conteúdo multinível externo (§19–§21) |
| `docs/contratos/contrato_json_console.md` | Fronteira declarativa vigente do envelope do console e do documento externo multinível — schema semântico (§12, ADR-0027), apresentações e modos (§13, ADR-0028) |
| `docs/nomenclatura/32_CONSOLE.md` | Terminologia canônica de console, foco, cursor, seleção única, seleção múltipla, navegação toroidal por eixo e paginação |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | Fronteira entre apresentação multinível (modos verboso/não verboso, D23) e a navegação do `ITEM-0007`, explicitamente deferida a este ciclo |

---

## 3. Decisão explícita do usuário

As treze decisões abaixo são fechadas e transportadas integralmente. Nenhuma
alternativa é escolhida por este documento.

O patch P04 acrescenta D-MULTI-07-P04, que restringe estruturalmente a
selecionabilidade: descendente selecionável implica todos os ancestrais
estruturais selecionáveis, sem alterar a política de navegação ou a
reconciliação já fechada por D-MULTI-06-P03.

### D-MULTI-01 — Escopo do ciclo

```yaml
escopo:
  - politicas_explicitas_de_navegacao
  - foco_entre_consoles
  - cursor_dentro_do_console
  - nivel_unico
  - tabela
  - arvore_colapsavel
  - selecao_multinivel
  - dois_niveis_por_foco
  - semantica_de_espaco_associada_a_essas_politicas
  - integracao_com_a_apresentacao_de_selecao_ja_existente
```

O ciclo trata somente navegação multinível do console, restrita aos itens
acima. Nenhum outro comportamento é objeto desta ADR.

### D-MULTI-02 — Regras transversais

```yaml
tab_shift_tab: movimenta_foco_entre_consoles
setas: movimentam_cursor_dentro_do_console_focalizado_quando_a_politica_permitir
chip_navegar: somente_indicador_de_disponibilidade_de_navegacao_pelas_setas
foco_cursor_selecao: mecanismos_distintos
politica_de_navegacao: declarada_explicitamente_nao_inferida_dos_dados
estrutura_dos_dados: nao_escolhe_automaticamente_a_politica
item_visivel_nao_navegavel: nao_recebe_cursor
fixture: sem_comportamento_especial_derivado_do_nome
apresentacao_visual_de_selecao: reutilizar_a_ja_existente
nova_linguagem_visual_de_selecao: proibida
```

### D-MULTI-03 — `nivel_unico`

```yaml
comportamento: preservar_o_vigente
quando_navegavel:
  setas: quatro_setas
  topologia: toroidal_por_eixo_conforme_autoridade_vigente
  celulas_vazias: ignoradas
  mecanismo_vigente_de_nivel_unico: mantido
  tab_shift_tab: continuam_trocando_foco_entre_consoles
redesenho: proibido
```

### D-MULTI-04 — `tabela`

```yaml
tabela:
  participa_do_foco: false
  possui_cursor_entre_linhas: false
  setas_navegam_pelas_linhas: false
  exibe_chip_navegar: false
  fallback_para_nivel_unico: false
  declaracao_incompativel_de_tabela_navegavel: falha_focal
```

### D-MULTI-05 — `arvore_colapsavel`

```yaml
natureza: arvore_hierarquica_navegavel_sem_selecao
setas_cima_baixo: percorrem_a_sequencia_hierarquica_atualmente_visivel
ramo_fechado:
  descendentes: retirados_do_percurso
  ramo: permanece_item_corrente
espaco_sobre_ramo: abre_ou_fecha_o_ramo
selecao: ausente
todos: ausente
enter: nenhuma_semantica_criada
```

### D-MULTI-06 — `selecao_multinivel`

```yaml
profundidade: arbitraria
topologia: unica_reunindo_todos_os_niveis
toroides_independentes:
  por_pai: proibido
  por_nivel: proibido
  por_ramo: proibido
apresentacao: pode_ocupar_multiplas_colunas_quando_a_geometria_vigente_ja_permitir
hierarquia: altera_o_alcance_de_espaco_nao_divide_a_navegacao
espaco_sobre_folha:
  nao_selecionada_para_selecionada: true
  selecionada_para_nao_selecionada: true
espaco_sobre_pai:
  atua_recursivamente_sobre_todos_os_descendentes_selecionaveis_em_qualquer_profundidade: true
  inclusao: seleciona_todos
  remocao: remove_todos
  itens_nao_selecionaveis: sem_alteracao
estado_selecao:
  item_selecionavel:
    estado: binario
    apresentacao: tg_existente
  item_nao_selecionavel:
    estado: ausente
    apresentacao: tg_ausente
    participa_da_unanimidade: false
  pai_selecionavel:
    selecionado_quando: todos_os_filhos_selecionaveis_imediatos_estao_selecionados
    nao_selecionado_quando: existe_pelo_menos_um_filho_selecionavel_imediato_nao_selecionado
    estado_parcial_ou_indeterminado: proibido
propagacao_ascendente:
  apos_toggle_de_folha: reconciliar_ancestrais_de_baixo_para_cima
  alcance: recursivo_ate_a_raiz
  filho_desmarcado: desmarca_pais_e_ancestrais_que_deixarem_de_satisfazer_unanimidade
apos_propagacao_descendente: reconciliar_pais_de_baixo_para_cima
apresentacao_de_selecao: reutilizar_a_ja_existente
```

A ampliação `D-MULTI-06-P03 — estado selecionado derivado e propagação
bidirecional na hierarquia` integra a regra acima à decisão vigente. Ela não
introduz alternativa, estado parcial, contador, seleção independente do pai,
novo símbolo ou política específica por profundidade.

Em `selecao_multinivel`, a regra vale para raiz selecionável, pai intermediário
selecionável e folha selecionável. Item não selecionável não recebe estado de
seleção nem `tg` e é ignorado no cálculo de unanimidade. A seleção manual de
todos os filhos selecionáveis imediatos marca o pai; a desseleção de qualquer
filho desmarca o pai e os ancestrais afetados, sempre recursivamente até a
raiz. Espaço sobre pai continua selecionando ou removendo recursivamente todos
os descendentes selecionáveis, sem alterar os não selecionáveis; depois disso,
os pais são reconciliados de baixo para cima. A regra vale em profundidade
arbitrária, sem semântica especial para nível 1, 2 ou 3.

Para a demonstração futura de H-0054, a fixture deve conter pelo menos três
pais de nível 1. O primeiro deve conter dois pais de nível 2 selecionáveis,
cada um com mais de uma folha selecionável. O caso não selecionável deve
estar no segundo ramo, cujo pai de nível 1 (`2.`) é selecionável e possui
`tg`; abaixo dele deve existir um item explicitamente não selecionável, sem
`tg` e sem descendentes selecionáveis. Deve existir um terceiro ramo para
diversidade/demonstração. A fixture deve permitir demonstrar seleção de cima
para baixo, seleção manual de baixo para cima e desseleção com preservação dos
ramos independentes.

### D-MULTI-07-P04 — coerência estrutural de selecionabilidade

```yaml
regra:
  descendente_selecionavel: todo_ancestral_estrutural_ate_a_raiz_selecionavel
  pai_com_ao_menos_um_descendente_selecionavel:
    selecionavel: true
    estado: binario
    apresentacao: tg_existente
  item_nao_selecionavel:
    estado: ausente
    apresentacao: tg_ausente
    participa_do_conjunto_selecionado: false
    participa_da_unanimidade: false
    subarvore: integralmente_nao_selecionavel
    pode_ser: folha_ou_pai_de_conteudo_integralmente_nao_selecionavel
  pai_nao_selecionavel_com_descendente_selecionavel:
    configuracao: invalida_e_incoerente
    comportamento_funcional: nao_suportado
```

Em `selecao_multinivel`, a selecionabilidade é estruturalmente coerente em
profundidade arbitrária: se um nó possui ao menos um descendente
selecionável, o próprio nó e todos os seus ancestrais estruturais até a raiz
devem ser selecionáveis. Toda raiz ou pai intermediário que contém seleção
abaixo dela possui estado binário e `tg`, e participa da seleção segundo as
regras de D-MULTI-06-P03.

Um item declarado não selecionável não possui estado de seleção, não recebe
`tg`, não entra no conjunto selecionado e não participa da unanimidade. Ele
pode ser uma folha ou um pai cujo conteúdo abaixo dele seja integralmente não
selecionável, mas não pode introduzir uma subárvore com itens selecionáveis.
Logo, `item não selecionável → toda sua subárvore é não selecionável`.

O cenário `pai não selecionável + descendente selecionável` é configuração
inválida/incoerente, e não comportamento funcional suportado. Não há Espaço
recursivo a definir para esse caso. Para pais válidos com descendentes
selecionáveis, o pai é selecionável, possui `tg` e Espaço opera pela política
descendente já vigente; D-MULTI-06-P03 continua governando a reconciliação
pai↔filhos.

Na fixture H-0054, o segundo ramo deve ser lido como `2.` — pai de nível 1
selecionável — contendo um item explicitamente não selecionável. O pai `2.`
participa normalmente da seleção e possui `tg`; o item não selecionável não
possui `tg` e não possui descendentes selecionáveis. O caso negativo correto
é um pai selecionável com filho selecionável e item não selecionável: o item
permanece fora da seleção recursiva e não impede a unanimidade calculada
somente sobre os filhos selecionáveis.

### D-MULTI-07 — `dois_niveis_por_foco`: estrutura

```yaml
niveis:
  nivel_1: pais
  nivel_2: filhos_diretos_de_cada_pai
terceiro_nivel: invalido
toroide_de_pais: unico_reunindo_todos_os_pais_navegaveis
toroide_de_filhos: proprio_por_pai
filhos_de_pais_distintos: nunca_pertencem_ao_mesmo_toroide
toroide_de_filhos_ativo: determinado_pelo_pai_corrente
```

### D-MULTI-08 — `dois_niveis_por_foco`: entrada e retorno

```yaml
nivel_dos_pais:
  espaco: entra_no_toroide_dos_filhos_do_pai_corrente
nivel_dos_filhos:
  esc: retorna_ao_toroide_dos_pais
setas: operam_somente_no_toroide_atualmente_ativo
```

### D-MULTI-09 — `dois_niveis_por_foco`: escolha obrigatória

```yaml
cada_pai: deve_possuir_um_filho_selecionado
escolha:
  exclusividade: exatamente_um_filho_por_pai
  selecionar_outro_filho: transfere_a_selecao_para_o_novo_filho
  espaco_sobre_filho_ja_selecionado: nao_remove_a_selecao_mantem_o_estado
  interacao_por_espaco: nunca_pode_deixar_o_pai_sem_filho_selecionado
cursor_e_escolha_do_filho: mecanismos_independentes
nomenclatura:
  termo_canonico_selecao_unica_ADR_0031: nao_reutilizar_para_este_mecanismo
  formulacao_no_novo_dominio: "seleção exclusiva obrigatória de filho por pai"
  redefinicao_do_termo_canonico_preexistente: proibida
apresentacao_visual: reutilizar_a_selecao_ja_existente
```

### D-MULTI-10 — Paginação

```yaml
autoridade_consumida: ADR-0041_paginacao_universal_por_pageup_e_pagedown
regra_concorrente_de_paginacao: proibida
cursor: sem_semantica_implicita_de_troca_de_pagina
```

### D-MULTI-11 — Demonstração exigida futuramente

```yaml
exigencia_de_demonstracao_real_em_tty:
  aplicacao_e_handoffs_devem_preservar: true
  por_politica_navegavel:
    - console_focalizado
    - cursor_visivel
    - item_corrente_distinguivel
    - movimento_efetivo_pelas_teclas_previstas
    - chip_navegar_quando_as_setas_estiverem_disponiveis
navegacao_em_mais_de_um_eixo:
  fixture: deve_possuir_geometria_que_efetivamente_demonstre_esses_eixos
  uma_unica_coluna: nao_demonstra_navegacao_horizontal
tabela:
  demonstracao_deve_confirmar: ausencia_de_cursor_e_de_chip_navegar
execucao_da_demonstracao_nesta_etapa: nao_realizada_esta_ADR_apenas_registra_o_criterio
```

### D-MULTI-12 — Forma declarativa da política

`politica_navegacao` permanece um objeto. Dentro dele, o campo discriminador
canônico é `tipo`, sem segunda forma alternativa de declaração:

```json
"politica_navegacao": {
  "navegavel": true,
  "tipo": "dois_niveis_por_foco"
}
```

O campo `navegavel` mantém sua semântica vigente. O campo `tipo` identifica
explicitamente a política aplicável, com os únicos valores fechados
`nivel_unico`, `tabela`, `arvore_colapsavel`, `selecao_multinivel` e
`dois_niveis_por_foco`.

### D-MULTI-13 — Compatibilidade com configurações existentes

Quando `politica_navegacao.tipo` estiver ausente, a configuração é
interpretada como `tipo = nivel_unico`. A ausência de `tipo`, por si só, não
torna a configuração inválida; a regra preserva a compatibilidade e o
comportamento vigente de nível único, permitindo a introdução incremental do
discriminador. Este fallback se aplica somente à ausência do novo campo. A
política não é inferida da estrutura dos dados, da apresentação, do nome da
fixture ou de qualquer outro atributo.

---

## 4. Decisão

Ficam adotadas, para a navegação multinível do console, as regras abaixo,
fechadas por decisão explícita do usuário e sem alternativa de desenho em
aberto.

### 4.1 Políticas de navegação

O console de conteúdo multinível opera sob uma de cinco políticas de
navegação, declaradas explicitamente e nunca inferidas da estrutura dos
dados (D-MULTI-02). A declaração mantém `politica_navegacao` como objeto e
usa o campo discriminador canônico `tipo`, com os valores fechados
`nivel_unico`, `tabela`, `arvore_colapsavel`, `selecao_multinivel` e
`dois_niveis_por_foco` (D-MULTI-12). Quando `tipo` estiver ausente, aplica-se
exclusivamente o fallback de compatibilidade `nivel_unico`; essa ausência não
é erro por si só (D-MULTI-13). O campo `navegavel` mantém sua semântica
vigente. Não existe segunda forma de declaração.

`nivel_unico` (comportamento vigente, preservado sem redesenho — D-MULTI-03),
`tabela` (apresentação passiva, sem foco, sem cursor, sem chip `[✥]` —
D-MULTI-04), e as três políticas fechadas por este ciclo para conteúdo
hierárquico — `arvore_colapsavel` (D-MULTI-05), `selecao_multinivel`
(D-MULTI-06) e `dois_niveis_por_foco` (D-MULTI-07 a D-MULTI-09) — mantêm suas
semânticas respectivas. A estrutura dos dados, a apresentação, o nome da
fixture ou qualquer outro atributo não escolhe automaticamente a política.

### 4.2 Regras transversais

Tab e Shift+Tab movimentam o foco entre consoles; as quatro setas movimentam
o cursor dentro do console focalizado quando a política aplicável permitir.
`[✥]` permanece exclusivamente o indicador de disponibilidade de navegação
pelas setas — não aciona movimento por si. Foco, cursor e seleção
permanecem três mecanismos distintos, como já fixado pela ADR-0031 e pela
ADR-0034. Item visível não navegável nunca recebe cursor. A apresentação
visual de seleção já existente (`tg` com `●`/`○`, ver `docs/nomenclatura/
32_CONSOLE.md` §4.4) deve ser reutilizada integralmente; nenhuma nova
linguagem visual de seleção é criada por este ciclo.

### 4.3 `nivel_unico` — preservação integral

O comportamento vigente de `nivel_unico` — quatro setas, navegação toroidal
por eixo conforme a ADR-0031, células vazias ignoradas, Tab/Shift+Tab
trocando foco entre consoles — é preservado sem redesenho. Esta ADR não
introduz variação alguma no mecanismo já vigente para nível único.

### 4.4 `tabela` — apresentação passiva

A apresentação `tabela` não participa do foco, não possui cursor entre
linhas, não é percorrida pelas setas e não exibe `[✥]`. Não recebe fallback
para `nivel_unico`. Declaração incompatível — uma instância que tente marcar
`tabela` como navegável — é falha focal.

### 4.5 `arvore_colapsavel` — hierarquia navegável sem seleção

`arvore_colapsavel` é uma árvore hierárquica navegável sem seleção. As setas
↑ e ↓ percorrem a sequência hierárquica atualmente visível — a sequência
linear resultante da expansão e do recolhimento correntes dos ramos. Fechar
um ramo retira seus descendentes do percurso de navegação; o próprio ramo
fechado permanece como item corrente. Espaço sobre um ramo abre ou fecha
esse ramo. Esta política não possui seleção, não possui `Todos` e não cria
semântica de Enter.

### 4.6 `selecao_multinivel` — topologia única com Espaço recursivo e reconciliação bidirecional

A hierarquia de `selecao_multinivel` pode possuir profundidade arbitrária.
Todos os elementos navegáveis, independentemente do nível, participam de uma
única topologia de navegação — não existem toroides independentes por pai,
por nível ou por ramo. A apresentação pode ocupar múltiplas colunas quando a
geometria vigente já permitir isso, sem que este ciclo introduza nova
distribuição geométrica.

D-MULTI-07-P04 acrescenta a invariável estrutural de que um nó com ao menos
um descendente selecionável deve ser selecionável, assim como todos os seus
ancestrais estruturais até a raiz. Portanto, toda raiz e todo pai intermediário
que contenham seleção abaixo deles possuem estado binário e `tg`. Essa
restrição vale em profundidade arbitrária e é compatível com D-MULTI-06-P03:
ela não altera a derivação binária, a unanimidade dos filhos selecionáveis
imediatos, a reconciliação ascendente, a propagação descendente, a ausência de
estado parcial ou a topologia única.

Todo item declarado selecionável — raiz, pai intermediário ou folha — possui
estado binário de seleção e usa a apresentação `tg` já existente. Item não
selecionável não recebe estado de seleção, não recebe `tg` e não participa do
cálculo de unanimidade dos filhos selecionáveis.

A hierarquia altera o alcance de Espaço, não divide a navegação: sobre uma
folha selecionável, Espaço alterna entre não selecionada e selecionada, nos
dois sentidos. Um pai selecionável fica marcado exatamente quando todos os
seus filhos selecionáveis imediatos estão selecionados; fica desmarcado quando
existe pelo menos um filho selecionável imediato não selecionado. Não existe
estado parcial ou indeterminado.

Depois de qualquer toggle de folha, os pais são reconciliados de baixo para
cima. Selecionar manualmente todos os filhos selecionáveis imediatos marca o
pai e, quando aplicável, continua recursivamente até a raiz. Desmarcar um
filho desmarca o pai e os ancestrais que deixarem de satisfazer a unanimidade,
sem alterar ramos independentes.

Sobre um pai, Espaço atua recursivamente sobre todos os descendentes
selecionáveis em qualquer profundidade — inclui todos quando a ação
corresponde à inclusão, remove todos quando corresponde à remoção — e itens
não selecionáveis permanecem sem alteração. Após a propagação descendente,
os estados dos pais são derivados/reconciliados de baixo para cima pela mesma
regra de unanimidade. A apresentação de seleção já existente é reutilizada
integralmente; nenhum novo estado visual é criado.

Um pai não selecionável com descendente selecionável é configuração
inválida/incoerente, não comportamento funcional suportado. Um item declarado
não selecionável não possui estado de seleção, não recebe `tg`, não entra no
conjunto selecionado, não participa da unanimidade e não pode introduzir uma
subárvore com itens selecionáveis. Logo, item não selecionável implica
subárvore integralmente não selecionável; o item pode ser folha ou pai de
conteúdo também integralmente não selecionável. Para um pai válido com
descendentes selecionáveis, o pai é selecionável, possui `tg` e Espaço opera
pela política descendente já vigente. O caso negativo correto é:

```text
pai selecionável
├── filho selecionável
└── item não selecionável
```

O item não selecionável permanece sem `tg`, não é marcado pela seleção
recursiva e não impede a unanimidade calculada somente sobre os filhos
selecionáveis.

### 4.7 `dois_niveis_por_foco` — dois toroides e escolha exclusiva por pai

`dois_niveis_por_foco` possui exatamente dois níveis: nível 1, os pais; e
nível 2, os filhos diretos de cada pai. Um terceiro nível é inválido. Todos
os pais navegáveis formam um único toroide do nível 1; cada pai possui seu
próprio toroide de filhos, e filhos de pais distintos nunca pertencem ao
mesmo toroide. O toroide de filhos ativo é sempre determinado pelo pai
corrente.

No nível dos pais, Espaço entra no toroide dos filhos do pai corrente. No
nível dos filhos, Esc retorna ao toroide dos pais. As setas operam somente
no toroide atualmente ativo — nunca simultaneamente em ambos.

Enquanto o nível ativo for o toroide de filhos, essa especialização de Esc
possui precedência, nesse contexto específico, sobre a regra geral de Esc
associada à seleção existente: retorna ao toroide dos pais, preserva a
seleção exclusiva obrigatória de filho do pai, não limpa essa escolha e não
possui semântica de cancelamento. O pai não pode ficar sem filho escolhido.
Essa precedência não altera a semântica geral de Esc das demais políticas.

Cada pai deve possuir exatamente um filho selecionado, de forma exclusiva e
obrigatória: selecionar outro filho transfere a seleção para ele; Espaço
sobre o filho já selecionado não remove sua seleção — mantém o estado sem
alteração; a interação por Espaço nunca pode deixar um pai sem filho
selecionado. Cursor e escolha do filho permanecem mecanismos independentes:
mover o cursor entre filhos não transfere a escolha por si — a transferência
ocorre somente pelo acionamento de Espaço sobre o novo filho.

Este mecanismo — a escolha exclusiva obrigatória de filho por pai — não é
nomeado com o termo canônico "seleção única" da ADR-0031, porque naquele
domínio "seleção única" designa o item sob cursor, que muda automaticamente
com o cursor (ver §5.1 abaixo). Quando este mecanismo precisar ser nomeado,
usa-se a formulação semanticamente inequívoca **"seleção exclusiva
obrigatória de filho por pai"**, sem redefinir o termo canônico preexistente.
A apresentação visual reutiliza a apresentação de seleção já existente.

### 4.8 Subordinação à paginação universal (ADR-0041)

Este ciclo consome integralmente a autoridade universal de paginação por
`PageUp`/`PageDown` fixada pela ADR-0041 (D-PGU-01 a D-PGU-08), conforme já
antecipado por D-PGU-08 daquela ADR. Nenhuma regra concorrente de paginação
é criada. O cursor não ganha semântica implícita de troca de página em
nenhuma das políticas fechadas por este ciclo — a distinção entre paginação
e navegação, já fixada em `docs/nomenclatura/32_CONSOLE.md` §3 ("paginação é
independente da navegação"), permanece integralmente preservada.

### 4.9 Isolamento da tentativa multinível anterior

Existe uma tentativa multinível anterior preservada em branch de erro. Esta
ADR foi produzida sem abrir essa branch, sem ler código, relatórios, patches
ou QAs produzidos nela, sem comparar a solução aqui fechada com ela e sem
corrigir ou reaproveitar sua implementação. A capacidade é definida
novamente, integralmente a partir das autoridades vigentes listadas em
§2.3, e de nenhuma forma a partir de artefatos daquela tentativa.

---

## 5. Compatibilidade com navegação e seleção preexistentes

### 5.1 Distinções preservadas

| Par | Distinção preservada por esta ADR |
|---|---|
| Foco × cursor | Foco: qual console está ativo na sessão, movido por Tab/Shift+Tab; cursor: qual item está sob navegação dentro do console focado, movido pelas setas quando a política permitir (ADR-0031) — inalterado por esta ADR |
| Cursor × seleção | Cursor aponta um item; seleção é o conjunto ou o estado de marcação de itens — mecanismos independentes em todas as políticas fechadas por este ciclo, inclusive `selecao_multinivel` e `dois_niveis_por_foco` |
| Item lógico × linha física | O cursor de `arvore_colapsavel`, `selecao_multinivel` e `dois_niveis_por_foco` percorre item lógico — a sequência hierárquica atualmente visível ou o toroide ativo — não linha física do terminal (ADR-0031 §22.4) |
| Paginação × navegação | Paginação permanece consequência automática do conteúdo que não cabe na área disponível, regida pela ADR-0041; navegação multinível não define, substitui nem antecipa regra de paginação (§4.8) |
| Seleção múltipla existente (ADR-0034) × novo mecanismo exclusivo por pai (D-MULTI-09) | Seleção múltipla (`politica_selecao: multipla`, `[␣]`, `tg` com `●`/`○`) é o mecanismo geral de conjunto de IDs estáveis fechado pela ADR-0034; a escolha exclusiva obrigatória de filho por pai é um mecanismo distinto, próprio de `dois_niveis_por_foco`, que reutiliza a mesma apresentação visual sem se confundir com seleção múltipla nem com seleção única |

### 5.2 Não confundir "seleção única" (ADR-0031) com a escolha exclusiva por pai

O termo canônico "seleção única", fixado por `docs/nomenclatura/
32_CONSOLE.md` §4.5 e `contrato_console.md` §22.7, designa exclusivamente o
único item sob cursor em console de nível único — muda automaticamente com o
cursor, sem toggle, sem persistência como conjunto. Esta ADR não redefine
esse termo. Mudar o cursor entre filhos em `dois_niveis_por_foco` não
transfere automaticamente a escolha do filho — a transferência ocorre
somente por Espaço (§4.7, D-MULTI-09).

### 5.3 Integração com a apresentação de seleção já existente

Todas as políticas que possuem seleção (`selecao_multinivel`,
`dois_niveis_por_foco`) reutilizam a apresentação visual de seleção já
existente — `tg` com `●`/`○`, conforme `docs/nomenclatura/32_CONSOLE.md`
§4.4. Nenhuma nova linguagem visual de seleção é criada. `arvore_colapsavel`
e `tabela` não possuem seleção e, portanto, não exibem `tg` em modo de
seleção ativa. Em `selecao_multinivel`, a mesma apresentação binária vale
para folhas e pais selecionáveis; itens não selecionáveis permanecem sem
estado e sem `tg`, e o estado do pai é derivado dos filhos, não uma seleção
independente desconectada deles.

---

### 5.4 Declaração e compatibilidade da política

Configurações novas declaram a política dentro do objeto
`politica_navegacao`, pelo campo `tipo`. Configurações existentes que não
possuem esse campo são compatíveis e equivalem a `nivel_unico`; não se exige
que a ausência seja tratada como configuração inválida. Essa regra não
redefine `navegavel`, não cria outra forma de declaração e não autoriza
inferência de política por dados, apresentação, nome de fixture ou qualquer
outro atributo.

## 6. Relação com a ADR-0041

A ADR-0041 fixou, de forma universal, que toda paginação comum do
Orquestrador — presente ou futura — usa exclusivamente `PageUp`/`PageDown` e
a representação `[PgUp][PgDn] Páginas`, e que a navegação multinível futura
deve consumir essa autoridade sem definir comandos próprios de paginação
(D-PGU-08). Esta ADR cumpre essa condição integralmente (§4.8): nenhuma
tecla, notação ou regra de paginação é criada ou reaberta por este ciclo. A
independência de página por console (ADR-0038 D-PAG-13; `contrato_console.
md` §24.10) e a distinção entre paginação e navegação (`docs/nomenclatura/
32_CONSOLE.md` §3) permanecem vigentes e aplicáveis, sem alteração, às
políticas multinível fechadas por esta ADR.

---

## 7. Consequências

### Positivas

- Fecha, para as cinco políticas explícitas de navegação do console
  (`nivel_unico`, `tabela`, `arvore_colapsavel`, `selecao_multinivel`,
  `dois_niveis_por_foco`), uma autoridade documental única sobre cursor,
  percurso e semântica de Espaço.
- Fecha a declaração das cinco políticas no objeto `politica_navegacao`, com
  `tipo` como discriminador canônico e fallback de compatibilidade para
  `nivel_unico` quando o campo estiver ausente.
- Preserva integralmente o comportamento vigente de `nivel_unico` e a
  passividade já esperada de `tabela`, evitando redesenho de capacidades já
  fechadas pela ADR-0031, pela ADR-0034 e pela ADR-0038/ADR-0041.
- Nomeia de forma inequívoca a escolha exclusiva obrigatória de filho por
  pai, evitando colisão terminológica com "seleção única" (ADR-0031) e
  preservando a integridade do termo canônico preexistente.
- Fecha, em `selecao_multinivel`, o estado binário derivado dos pais e a
  reconciliação recursiva de baixo para cima, tornando demonstrável a
  bidirecionalidade entre seleção manual de folhas e seleção recursiva de
  pais.
- Fecha a coerência estrutural de selecionabilidade: descendente selecionável
  implica todos os ancestrais até a raiz selecionáveis, enquanto uma subárvore
  não selecionável não pode conter seleção. Suporte específico a pai não
  selecionável com descendentes selecionáveis deixa de ser requisito e deverá
  ser removido ou reconciliado na futura aplicação da implementação.
- Fixa a subordinação integral à autoridade universal de paginação da
  ADR-0041, evitando qualquer regra concorrente de paginação neste ciclo ou
  em capacidades futuras que herdem desta ADR.
- Define a capacidade novamente a partir das autoridades vigentes, sem
  qualquer dependência da tentativa multinível anterior preservada em
  branch de erro — isolamento explícito e verificável.

### Custos e restrições

- Exigirá, na aplicação documental futura, a propagação das políticas
  `arvore_colapsavel`, `selecao_multinivel` e `dois_niveis_por_foco` para
  `contrato_console.md` e `contrato_json_console.md`, além da terminologia
  correspondente em `docs/nomenclatura/32_CONSOLE.md` e, quando material, em
  `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`.
- Introduz uma dependência documental explícita: nenhuma implementação deste
  ciclo pode antecipar `Pai: filho_ativo`, nova geometria, Enter, execução,
  confirmação, cancelamento, persistência ou prévia — capacidades reservadas
  a `ITEM-0023` e `ITEM-0024`.
- Exigirá, na aplicação e nos handoffs futuros, fixtures com geometria
  suficiente para demonstrar navegação em mais de um eixo quando aplicável,
  conforme o critério de demonstração de D-MULTI-11 (§8).
- Exigirá, na aplicação e no H-0054, fixture hierárquica com três pais de
  nível 1, dois pais de nível 2 no primeiro ramo, múltiplas folhas em cada um,
  ramo não selecionável separado e terceiro ramo, além dos cenários de
  propagação para baixo, reconciliação para cima e desseleção.

---

## 8. Itens fora de escopo

- `Pai: filho_ativo` — apresentação do filho ativo promovido junto ao pai
  (reservado a `ITEM-0023`).
- Promoção visual do filho selecionado para junto do pai.
- Novos estados visuais `○`, `◎` ou `●`, ou nova apresentação visual de
  seleção.
- Nova distribuição geométrica de grupos, compactação ou otimização de
  layout, ou nova política de quebra entre grupos (reservados a
  `ITEM-0024`).
- Enter, execução, confirmação, cancelamento, persistência, prévia ou
  qualquer ação posterior à seleção.
- Definição ou aplicação de nova regra de paginação — permanece
  integralmente subordinada à ADR-0041 (§4.8, §6).
- Qualquer leitura, comparação ou reaproveitamento da tentativa multinível
  anterior preservada em branch de erro (§4.9).
- Aplicação documental aos contratos e módulos de nomenclatura afetados,
  criação de handoff, implementação, testes e demonstração em TTY — etapas
  distintas, sujeitas a QA favorável desta ADR.
- H-0053 e H-0055 permanecem preservados e fora do escopo deste patch; não há
  alteração de `arvore_colapsavel`, `dois_niveis_por_foco`, paginação,
  PageUp/PageDown, cursor, foco, Enter, execução, confirmação ou persistência.
- D-MULTI-07-P04 também não altera a barra, os símbolos existentes ou a
  apresentação `tg`; preserva a barra e `tg` vigentes e não cria nova
  linguagem visual, geometria ou política de navegação.

---

## 9. Critérios para aplicação e demonstração

- [ ] `docs/contratos/contrato_console.md` e `docs/contratos/
  contrato_json_console.md` propagam as cinco políticas de navegação
  (`nivel_unico`, `tabela`, `arvore_colapsavel`, `selecao_multinivel`,
  `dois_niveis_por_foco`) exatamente como fechadas nesta ADR, sem introduzir
  alternativa não decidida aqui.
- [ ] `politica_navegacao` permanece um objeto e usa exatamente `tipo` como
  discriminador, sem segunda forma de declaração.
- [ ] `tipo` aceita somente `nivel_unico`, `tabela`, `arvore_colapsavel`,
  `selecao_multinivel` e `dois_niveis_por_foco`.
- [ ] A ausência de `politica_navegacao.tipo` equivale a `nivel_unico` e não
  é erro por si só.
- [ ] `politica_navegacao.navegavel` mantém sua semântica vigente; nenhuma
  regra adicional de combinação entre `navegavel` e `tipo` é introduzida.
- [ ] A política não é inferida da estrutura dos dados, da apresentação, do
  nome da fixture ou de qualquer outro atributo.
- [ ] `nivel_unico` é propagado como preservação, sem alteração do
  mecanismo vigente.
- [ ] `tabela` é propagada como apresentação passiva, com falha focal
  explícita para declaração incompatível de tabela navegável.
- [ ] A escolha exclusiva obrigatória de filho por pai não é registrada com
  o termo canônico "seleção única" em nenhum documento aplicado.
- [ ] Nenhum terceiro nível é admitido em `dois_niveis_por_foco`.
- [ ] Nenhuma semântica de Enter é criada para as políticas fechadas por
  esta ADR.
- [ ] `Pai: filho_ativo` e nova distribuição geométrica de grupos não são
  antecipados pela aplicação nem pelos handoffs deste ciclo.
- [ ] A paginação aplicada a instâncias multinível permanece exclusivamente
  a da ADR-0041 — nenhum comando, tecla ou notação concorrente é introduzido.
- [ ] A branch de erro que preserva a tentativa multinível anterior não é
  aberta, lida, comparada ou reaproveitada em nenhuma etapa posterior deste
  ciclo.
- [ ] Cada política navegável, quando aplicada e implementada, é demonstrada
  em TTY real com console focalizado, cursor visível, item corrente
  distinguível, movimento efetivo pelas teclas previstas e `[✥]` quando as
  setas estiverem disponíveis (D-MULTI-11).
- [ ] Quando houver navegação em mais de um eixo, a fixture de demonstração
  possui geometria que efetivamente demonstra esses eixos — uma única
  coluna não é aceita como demonstração de navegação horizontal.
- [ ] Para `tabela`, a demonstração confirma explicitamente a ausência de
  cursor e de `[✥]`.
- [ ] Em `selecao_multinivel`, toda folha e todo pai declarados selecionáveis
  possuem estado binário apresentado por `tg`; itens não selecionáveis não
  possuem estado, não recebem `tg` e são ignorados na unanimidade.
- [ ] Em `selecao_multinivel`, qualquer descendente selecionável implica que
  o nó e todos os ancestrais estruturais até a raiz sejam selecionáveis; pai
  válido com conteúdo selecionável possui `tg`.
- [ ] Pai não selecionável com descendente selecionável é configuração
  inválida/incoerente e não possui comportamento funcional suportado; não há
  Espaço recursivo definido para esse cenário.
- [ ] Item não selecionável só é folha ou pai de conteúdo integralmente não
  selecionável; permanece fora do conjunto selecionado e da unanimidade.
- [ ] Pai selecionável marcado significa que todos os seus filhos
  selecionáveis imediatos estão marcados; um único filho selecionável
  desmarcado deixa o pai desmarcado, sem estado parcial ou indeterminado.
- [ ] O toggle manual de folhas reconcilia pais e ancestrais de baixo para
  cima; a desseleção desmarca todos os ancestrais afetados e preserva ramos
  independentes.
- [ ] Espaço em pai propaga a seleção/remoção a todos os descendentes
  selecionáveis e, depois, reconcilia os pais de baixo para cima.
- [ ] A fixture de H-0054 contém pelo menos três pais de nível 1; o primeiro
  contém pelo menos dois pais de nível 2, cada qual com mais de uma folha
  selecionável; o segundo ramo possui o pai `2.` selecionável, com `tg`, e um
  item explicitamente não selecionável sem descendentes selecionáveis; há um
  terceiro ramo para diversidade/demonstração.
- [ ] O caso negativo demonstrado é pai selecionável com filho selecionável e
  item não selecionável; o item não selecionável permanece sem `tg`, não é
  marcado pela seleção recursiva e não impede a unanimidade dos filhos
  selecionáveis.
- [ ] A demonstração futura cobre: Espaço em `1.` marcando `1.1`, `1.2` e
  `1.`; seleção manual de `1.1.1`/`1.1.2` e dos filhos de `1.2` marcando os
  pais e depois `1.`; e desseleção de uma folha desmarcando apenas os
  ancestrais afetados.
- [ ] H-0053 e H-0055 não são alterados por esta decisão.
- [ ] Nenhuma implementação de código é feita nesta etapa de ADR.
- [ ] Nenhum handoff é criado nesta etapa de ADR.

---

## 10. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR. As decisões
D-MULTI-01 a D-MULTI-13 constituem decisão já fechada fornecida ao autor
documental; este documento não escolhe entre opções nem introduz
arquitetura, schema, política, representação visual ou fluxo de execução
além do que foi explicitamente decidido.

---

## 11. Bloqueios

nenhum
