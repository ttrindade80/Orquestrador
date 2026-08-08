---
name: ADR-0041-paginacao-universal-por-pageup-e-pagedown
description: "Padroniza universalmente os controles de paginação interativa do Orquestrador: entradas exclusivas PageUp/PageDown, representação canônica [PgUp][PgDn] Páginas na barra de menus, extinção de qualquer função de paginação para '<', '>', ',' e '.', aplicação a toda capacidade presente ou futura, e preservação integral das demais regras de paginação limitada já fixadas pela ADR-0038"
metadata:
  type: adr
  status: aceita
  id: ADR-0041
  data: "2026-08-07"
  substitui: null
rastreabilidade:
  decisao_usuario: "D-PGU-01 a D-PGU-08 — paginação interativa passa a usar exclusivamente as teclas físicas PageUp (página anterior) e PageDown (próxima página); representação canônica na barra de menus passa a ser [PgUp][PgDn] Páginas; os caracteres '<', '>', ',' e '.' deixam de ter qualquer função de paginação, sem status de alias, atalho ou fallback; a mudança é universal, aplicável a toda paginação comum do Orquestrador presente ou futura, não apenas a consoles multinível; as demais regras da paginação limitada da ADR-0038 permanecem integralmente vigentes; esta ADR especializa/substitui somente as definições de tecla e representação visual, sem reabrir as demais decisões D-PAG; a futura navegação multinível deve consumir esta autoridade universal, sem definir comandos próprios de paginação"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0003
    - ITEM-0007
  contratos_afetados:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
  handoffs_bloqueados: []
---

# ADR-0041 — Paginação universal por PageUp e PageDown

## 1. Status

`aceita`

```yaml
status_da_adr: aceita
qa_da_adr:
  resultado: ADR_APPROVED
  relatorio: docs/relatorios/RELATORIO_QA_ADR-0041.md
patch:
  aplicado: true
  id: P01
  relatorio: docs/relatorios/RELATORIO_PATCH_ADR-0041_P01.md
aplicacao_documental:
  executada: true
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0041.md
  qa_da_aplicacao: ADR_APPLICATION_APPROVED
  relatorio_qa_aplicacao: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0041.md
handoff:
  id: H-0051
  qa: H1_HANDOFF_APPROVED
implementacao:
  status: IMPLEMENTED
  relatorio: docs/relatorios/IMP-0051-paginacao-universal-pageup-pagedown.md
  qa: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0051.md
validacao_manual:
  status: MANUAL_VALIDATION_APPROVED
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0051.md
```

Esta ADR foi criada a partir de oito decisões fechadas fornecidas ao autor
documental (D-PGU-01 a D-PGU-08). Nenhuma delas foi escolhida, reaberta ou
alterada por este documento. O QA da ADR foi concluído com resultado
`ADR_APPROVED` após o patch `P01`, sem achados abertos. A aplicação
documental propagou as decisões aos contratos e módulos de nomenclatura
afetados, com QA da aplicação `ADR_APPLICATION_APPROVED`. O handoff
`H-0051` foi implementado, com QA técnico sem achados e validação manual
aprovada em TTY real (`6/6`).

---

## 2. Contexto

### 2.1 Estado material ao início deste ciclo

A ADR-0038 fechou a paginação interativa limitada do `console` (D-PAG-01 a
D-PAG-14), incluindo, em D-PAG-14, as entradas de teclado aceitas para
página anterior (`,` e `<`) e para próxima página (`.` e `>`), com os chips
exibidos `[<]` e `[>]`. Essa decisão foi propagada a
`contrato_console.md` §24.11, `contrato_barra_de_menus.md` §8.3 e §24.4, e
`contrato_chip.md` §7 e §9, além de registrada em
`docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` §4.4.2. As demais treze
decisões da ADR-0038 — topologia limitada sem wrap entre páginas, cursor no
primeiro item navegável da página de destino após troca explícita, páginas
sem item navegável, universo por página do chip `[✥]`, preservação de página
no retorno por foco, repaginação por redimensionamento e mudança de modo,
interação entre filtro e paginação, interação entre atualização genérica dos
dados e paginação, indicador `página X/Y` inclusive para conjunto vazio, e
independência de página por console — permanecem vigentes e não são objeto
desta ADR.

O `docs/backlog.md` registra, como pré-requisito do `ITEM-0007` (navegação
multinível do console), a conclusão prévia de "um ciclo universal que
substitui toda paginação do Orquestrador por `PageUp`/`PageDown` e chips
`[PgUp]`/`[PgDn]`" — ou seja, a futura navegação multinível já está
condicionada, pelo próprio backlog, a esta padronização universal antes de
poder definir sua própria especificação.

### 2.2 Problema

Sem esta ADR, a única autoridade vigente para as entradas de paginação
continuaria sendo D-PAG-14 da ADR-0038 (`,`/`<` e `.`/`>`, chips `[<][>]`), e
não haveria nenhuma autoridade documental universal, aplicável a toda
paginação comum do Orquestrador — presente ou futura —, da qual capacidades
futuras (a começar pela navegação multinível do `ITEM-0007`) pudessem herdar
teclas e representação visual sem definir comandos de paginação próprios.
Esta ADR responde a essa lacuna por meio de oito decisões fechadas (D-PGU-01
a D-PGU-08), especializando exclusivamente a tecla física e a representação
visual dos controles de paginação já fixados pela ADR-0038, sem tocar em
nenhuma outra regra de paginação limitada.

### 2.3 Autoridades consultadas

| Documento | Papel |
|---|---|
| `docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md` | Autoridade integral da paginação interativa limitada do console; fixa D-PAG-01 a D-PAG-14, das quais somente D-PAG-14 (entradas aceitas) e a notação `[<][>]` são especializadas por esta ADR |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | Distinção entre configuração concreta e estado de runtime; página permanece estado de runtime, não alterado por esta ADR |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Terminologia de paginação, indicador `página X/Y`, `paginação limitada`, `repaginação` e demais termos operacionais da ADR-0038, preservados integralmente |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Ordem fixa dos chips canônicos; condição de existência e notação de `[<][>]`; entradas aceitas de página anterior/próxima página (ADR-0038) |
| `docs/contratos/contrato_console.md` | §24.11 — entradas aceitas de página anterior/próxima página (D-PAG-14) |
| `docs/contratos/contrato_barra_de_menus.md` | §8.3 e §24 — notação `[<][>]`, topologia limitada, entradas aceitas |
| `docs/contratos/contrato_chip.md` | §7 e §9 — notação canônica `[<][>]`, regra de ativo/inativo, entradas aceitas |

---

## 3. Decisão explícita do usuário

As oito decisões abaixo são fechadas e transportadas integralmente. Nenhuma
alternativa é escolhida por este documento.

### D-PGU-01 — Teclas físicas exclusivas

```yaml
entradas_aceitas:
  pagina_anterior: ["PageUp"]
  proxima_pagina: ["PageDown"]
exclusividade: true
```

Toda paginação interativa do Orquestrador usa exclusivamente as teclas
físicas `PageUp` e `PageDown`. Nenhuma outra tecla ou caractere aciona
página anterior ou próxima página.

### D-PGU-02 — Semântica das teclas

```yaml
PageUp: pagina_anterior
PageDown: proxima_pagina
```

`PageUp` significa página anterior; `PageDown` significa próxima página.

### D-PGU-03 — Representação canônica na barra de menus

```yaml
representacao_canonica: "[PgUp][PgDn] Páginas"
associacao:
  "[PgUp]": PageUp
  "[PgDn]": PageDown
```

A representação canônica dos controles de paginação na barra de menus passa
a ser `[PgUp][PgDn] Páginas`, com `[PgUp]` associado à tecla `PageUp` e
`[PgDn]` associado à tecla `PageDown`. Esta notação substitui, em todos os
documentos normativos, a notação `[<][>]` fixada pela ADR-0038.

### D-PGU-04 — Extinção da função de paginação de `<`, `>`, `,` e `.`

```yaml
caracteres_sem_funcao_de_paginacao: ["<", ">", ",", "."]
status: NENHUM
  # não são alias
  # não são atalho
  # não são fallback de PageUp/PageDown
```

Os caracteres `<`, `>`, `,` e `.` deixam de possuir qualquer função de
paginação. Não são aliases, atalhos ou fallback de `PageUp`/`PageDown`. Essa
extinção é integral: nenhum desses caracteres aciona página anterior ou
próxima página sob nenhuma condição.

### D-PGU-05 — Universalidade da mudança

```yaml
escopo_de_aplicacao: TODA_PAGINACAO_COMUM_DO_ORQUESTRADOR
temporalidade: PRESENTE_E_FUTURA
restrito_a_consoles_multinivel: false
```

A mudança é universal: aplica-se a toda capacidade presente ou futura que
use a paginação comum do Orquestrador, não apenas a consoles multinível.
Não há paginação comum do Orquestrador excetuada desta padronização.

### D-PGU-06 — Preservação integral das demais regras de paginação limitada

```yaml
regras_preservadas_da_ADR-0038:
  - topologia_limitada_sem_wrap_entre_primeira_e_ultima_pagina        # D-PAG-01
  - controle_anterior_inativo_na_primeira_pagina                       # D-PAG-01
  - controle_seguinte_inativo_na_ultima_pagina                         # D-PAG-01
  - ambos_inativos_com_somente_uma_pagina                              # D-PAG-01, D-PAG-11
  - pagina_como_estado_de_runtime                                      # D-PAG-13; núcleo comum §4.7
  - troca_explicita_reposiciona_conforme_politica_vigente              # D-PAG-02
  - setas_de_navegacao_interna_nao_mudam_de_pagina                     # ADR-0031 D15; D-PAG-03
  - indicador_pagina_x_de_y                                            # D-PAG-11, D-PAG-12
  - regras_de_repaginacao_e_reconciliacao_vigentes                     # D-PAG-05 a D-PAG-10
```

Ficam integralmente preservadas as demais regras da paginação limitada já
vigentes pela ADR-0038: sem wrap entre primeira e última página; controle
anterior inativo na primeira página; controle seguinte inativo na última
página; ambos inativos quando existe somente uma página; página como estado
de runtime; troca explícita reposiciona conforme a política vigente; setas
de navegação interna não mudam de página; indicador `página X/Y`; e as
regras de repaginação e reconciliação vigentes (retorno por foco,
redimensionamento, mudança de modo, filtro e atualização genérica dos
dados). Nenhuma dessas regras é reaberta, alterada ou reinterpretada por
esta ADR.

### D-PGU-07 — Especialização limitada às teclas e à representação visual

```yaml
escopo_da_especializacao:
  - teclas_de_acionamento_da_paginacao
  - representacao_visual_dos_controles_de_paginacao
decisoes_D-PAG_reabertas: nenhuma
```

Esta ADR especializa/substitui somente as definições anteriores relativas
às teclas e à representação visual dos controles de paginação (D-PAG-14 e a
notação `[<][>]` correlata). Não reabre as demais decisões D-PAG da
ADR-0038.

### D-PGU-08 — Autoridade universal para navegação multinível futura

```yaml
navegacao_multinivel_futura:
  deve_consumir: AUTORIDADE_UNIVERSAL_DESTA_ADR
  pode_definir_comandos_proprios_de_paginacao: false
```

A futura navegação multinível deve consumir esta autoridade universal e não
definir comandos próprios de paginação. Qualquer especificação futura da
navegação multinível do `ITEM-0007` herda `PageUp`/`PageDown` e
`[PgUp][PgDn]` desta ADR, sem redefinir tecla ou notação.

---

## 4. Decisão

Fica adotado, para toda paginação interativa comum do Orquestrador, presente
ou futura, o seguinte modelo universal de tecla e representação visual,
fechado por decisão explícita do usuário e sem alternativa de desenho em
aberto:

**Tecla física exclusiva (D-PGU-01, D-PGU-02, D-PGU-04).** Toda paginação
interativa usa exclusivamente `PageUp` (página anterior) e `PageDown`
(próxima página). Os caracteres `<`, `>`, `,` e `.`, antes aceitos pela
ADR-0038 (D-PAG-14), deixam de ter qualquer função de paginação — não como
alias, não como atalho, não como fallback.

**Representação canônica na barra de menus (D-PGU-03).** A notação
`[<][>]` fixada pela ADR-0038 é substituída, em todos os documentos
normativos, por `[PgUp][PgDn] Páginas`, com `[PgUp]` associado a `PageUp` e
`[PgDn]` associado a `PageDown`.

**Universalidade e autoridade para o futuro (D-PGU-05, D-PGU-08).** A
padronização aplica-se a toda capacidade presente ou futura que use a
paginação comum do Orquestrador — não é uma regra específica de console
multinível. Toda especificação futura, a começar pela navegação multinível
do `ITEM-0007`, consome esta autoridade universal em vez de definir
comandos próprios de paginação.

**Preservação integral do restante da ADR-0038 (D-PGU-06, D-PGU-07).**
Nenhuma regra de topologia, cursor, universo de avaliação de `[✥]`,
indicador, repaginação, reconciliação ou independência por console fixada
pela ADR-0038 é alterada. Esta ADR especializa exclusivamente a tecla de
acionamento e a representação visual dos controles de paginação; nenhuma
outra decisão D-PAG-01 a D-PAG-14 é reaberta.

---

## 5. Consequências

### Positivas

- Fecha, de forma universal e antecipada, um pré-requisito documental já
  registrado pelo próprio `docs/backlog.md` para o `ITEM-0007`, evitando que
  a navegação multinível precise redefinir tecla ou notação de paginação.
- Elimina a ambiguidade e a sobreposição semântica dos caracteres `<`, `>`,
  `,` e `.`, hoje usados como entrada, com outros usos possíveis desses
  mesmos caracteres em capacidades futuras.
- Fixa uma autoridade única e explícita para tecla e representação visual de
  paginação, evitando que capacidades futuras infiram ou dupliquem essa
  decisão.
- Preserva integralmente o investimento já realizado na ADR-0038, no
  `H-0045` e na implementação e validação manual do `ITEM-0003`, restrito
  apenas à tecla e à notação.

### Custos e restrições

- Exigiu que a aplicação documental revisasse toda ocorrência textual de
  `,`, `<`, `.`, `>` e `[<][>]` relacionada a paginação nos contratos e
  módulos de nomenclatura afetados, sem alterar nenhuma outra regra
  colateral presente no mesmo trecho — aplicação e QA da aplicação
  concluídos.
- Introduz uma dependência documental explícita: nenhuma ADR futura de
  paginação (inclusive a do `ITEM-0007`) pode fixar tecla ou notação própria
  sem contrariar D-PGU-08.

### Artefatos potencialmente afetados pela aplicação

| Artefato | Aplicação necessária |
|---|---|
| `docs/contratos/contrato_console.md` | Atualizar §24.11 (entradas aceitas de página anterior/próxima página) para `PageUp`/`PageDown`; ajustar remissões que citam `,`/`<` e `.`/`>`. |
| `docs/contratos/contrato_barra_de_menus.md` | Atualizar §8.3 (linha de `[<][>]` na ordem fixa dos chips canônicos), §24.1 e §24.4 para a notação `[PgUp][PgDn]` e as novas entradas. |
| `docs/contratos/contrato_chip.md` | Atualizar §7 (lista de notações canônicas) e §9 (nota sobre `[<][>]`, entradas aceitas) para `[PgUp][PgDn]` e `PageUp`/`PageDown`. |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Atualizar §3, §4.3 (ordem fixa dos chips canônicos) e §4.4.2 (paginação limitada de `[<][>]`) para a notação e entradas canônicas desta ADR. |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Avaliar se algum termo cita a tecla ou notação anterior; o indicador `página X/Y` e a topologia limitada não são afetados. |
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0041 após QA favorável. |
| `docs/backlog.md` | Pré-requisito de paginação universal do `ITEM-0007` atualizado no fechamento do ciclo (ADR-0041 / H-0051). |

A tabela acima identificou os documentos cuja atualização decorreu da decisão
já fechada; a aplicação documental, o handoff `H-0051`, a implementação e a
validação manual foram concluídos neste ciclo.

---

## 6. Compatibilidade e transição

Esta ADR registra a decisão fechada; a aplicação documental, o handoff, a
implementação e a validação manual ocorreram em etapas posteriores do mesmo
ciclo. Após a aplicação, os contratos e módulos de nomenclatura listados na
seção 5 passaram a citar `PageUp`/`PageDown` e `[PgUp][PgDn]` como vigentes.

Não há migração automática de telas existentes além do manifesto do
`H-0051`: a paginação do `ITEM-0003` (`H-0045`) passou a operar com
`PageUp`/`PageDown` e `[PgUp][PgDn]` após a aplicação documental e a
implementação deste ciclo. Console sem `politica_paginacao` declarada
permanece fora do impacto desta ADR (`contrato_console.md` §12), por não
possuir paginação comum à qual a autoridade desta ADR se aplique. Console
com paginação de página única permanece integralmente submetido à
autoridade universal desta ADR (D-PGU-05), inclusive quando possui, no
momento, somente uma página: os controles, quando exibidos, usam a
representação canônica `[PgUp][PgDn] Páginas` (D-PGU-03), e permanecem
vigentes as regras já preservadas da ADR-0038 (D-PGU-06) — indicador
`página 1/1` e ambos os controles inativos. A existência de somente uma
página pode significar ausência de mudança comportamental de navegação
perceptível nesse console, mas nunca exclusão do escopo ou do impacto desta
ADR.

Esta ADR preserva integralmente:

- a topologia limitada, o destino do cursor na troca de página, as páginas
  sem item navegável, o universo do chip `[✥]` por página, a preservação de
  página no retorno por foco, a repaginação por redimensionamento e mudança
  de modo, a interação entre filtro e paginação, a interação entre
  atualização genérica dos dados e paginação, o indicador `página X/Y`
  inclusive para conjunto vazio, e a independência de página por console —
  todas já fixadas pela ADR-0038 (D-PAG-01 a D-PAG-13), sem nenhuma reabertura;
- a distinção entre existência declarativa (`regra_existencia`) e ativação
  dinâmica (`regra_ativo`) do chip, já fixada por `contrato_chip.md`;
- a distinção entre configuração concreta e estado de runtime já fixada por
  `docs/nomenclatura/01_NUCLEO_COMUM.md` — página permanece estado de
  runtime, não campo do `tela.json`.

---

## 7. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR. As decisões D-PGU-01 a
D-PGU-08 constituem decisão já fechada fornecida ao autor documental; este
documento não escolhe entre opções nem introduz arquitetura, schema ou
comportamento além do que foi explicitamente decidido.

---

## 8. Itens fora de escopo

- Alterar a lógica de cálculo das páginas.
- Alterar a topologia limitada já fixada pela ADR-0038.
- Alterar o cursor — destino, preservação ou reconciliação.
- Alterar a seleção múltipla ou sua persistência entre páginas.
- Implementar a navegação multinível do `ITEM-0007`.
- Alterar a distribuição geométrica de conteúdo ou de grupos.
- Criar novos controles de paginação além de `PageUp`/`PageDown`.
- Aplicação documental aos contratos e módulos de nomenclatura afetados —
  etapa distinta, sujeita a QA favorável desta ADR.
- QA da ADR, atualização de índice ou de backlog, criação de handoff,
  implementação, testes, stage e commit — fora desta execução.

---

## 9. Critérios para aplicação

- [x] `docs/contratos/contrato_console.md`, `docs/contratos/contrato_barra_de_menus.md`
  e `docs/contratos/contrato_chip.md` foram atualizados conforme a tabela de
  artefatos afetados (seção 5).
- [x] Somente os módulos proprietários da nomenclatura efetivamente afetados
  (`31`, e `21` se material) foram avaliados e, quando material, atualizados.
- [x] Nenhuma outra decisão D-PAG-01 a D-PAG-13 foi alterada durante a
  aplicação.
- [x] Nenhuma ocorrência residual de `,`, `<`, `.` ou `>` como entrada de
  paginação, nem de `[<][>]` como notação de paginação, permanece nos
  documentos aplicados.
- [x] `docs/adr/INDICE_ADR.md` foi atualizado somente após QA favorável desta
  ADR.
- [x] `docs/backlog.md` foi atualizado somente quando o fluxo documental
  determinar mudança material do pré-requisito do `ITEM-0007`.
- [x] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [x] Nenhum handoff foi criado na mesma etapa da aplicação documental.
- [x] Caminhos permanecem relativos à raiz do Orquestrador.
- [x] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [x] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [x] A aplicação foi submetida a QA independente.

---

## 10. Relação com a ADR-0038

A ADR-0038 é preservada quanto a todas as suas quatorze decisões (D-PAG-01 a
D-PAG-14), com uma única especialização pontual: D-PAG-14 (entradas
aceitas) e a notação `[<][>]` correlata, presente em `contrato_console.md`
§24.11, `contrato_barra_de_menus.md` §8.3/§24.1/§24.4,
`contrato_chip.md` §7/§9 e `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
§4.3/§4.4.2, são substituídas por `PageUp`/`PageDown` e `[PgUp][PgDn]`
(D-PGU-01 a D-PGU-04, D-PGU-07).

Nenhuma outra decisão da ADR-0038 é reaberta: a topologia limitada
(D-PAG-01), o destino do cursor após troca explícita de página (D-PAG-02),
a página sem item navegável (D-PAG-03), o universo do chip `[✥]`
(D-PAG-04), o retorno ao console por foco (D-PAG-05), a repaginação por
redimensionamento e mudança de modo (D-PAG-06), a interação entre filtro e
paginação (D-PAG-07 a D-PAG-09), a atualização genérica dos dados e a
precedência da ADR-0037 (D-PAG-10), o indicador de página (D-PAG-11,
D-PAG-12) e a independência de página por console (D-PAG-13) permanecem
integralmente vigentes, conforme D-PGU-06 e D-PGU-07.

A relação da ADR-0038 com a ADR-0031, a ADR-0034 e a ADR-0037 (seção 10 da
própria ADR-0038) não é afetada por esta ADR: nenhuma delas trata de tecla
de acionamento ou de notação visual de paginação.

---

## 11. Bloqueios

nenhum
