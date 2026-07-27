---
name: relatorio-aplicacao-adr-0031
description: Relatório de aplicação documental da ADR-0031 — navegação simples e seleção única em console de nível único
metadata:
  type: relatorio
  scope: orquestrador
  adr: ADR-0031
  data_aplicacao: "2026-07-25"
  resultado: ADR_APPLICATION_COMPLETED_AWAITING_QA
---

# Relatório de Aplicação Documental — ADR-0031

## 1. Identificação

| Campo | Valor |
|---|---|
| ADR | ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md |
| Título | Navegação simples e seleção única em console de nível único |
| Item do backlog | ITEM-0002 |
| Data de aplicação | 2026-07-25 |
| Resultado da QA da ADR | ADR_QA_APPROVED_WITH_NOTES |
| Relatório da QA da ADR | docs/relatorios/RELATORIO_QA_ADR-0031.md |
| Resultado desta aplicação | ADR_APPLICATION_COMPLETED_AWAITING_QA |

---

## 2. Resultado dos checks de portão

Todos os checks de portão foram verificados antes de qualquer alteração.

| # | Check | Resultado |
|---|---|---|
| G-1 | ADR-0031 existe em `docs/adr/` | PASSOU |
| G-2 | Status da ADR é `ADR_CREATED_AWAITING_QA` | PASSOU |
| G-3 | Relatório de QA existe (`RELATORIO_QA_ADR-0031.md`) | PASSOU |
| G-4 | Resultado da QA é `ADR_QA_APPROVED_WITH_NOTES` | PASSOU |
| G-5 | Não há handoff pendente desta ADR | PASSOU |
| G-6 | Stage git está limpo | PASSOU |
| G-7 | Não há implementação iniciada que dependa desta ADR | PASSOU |

---

## 3. Inputs lidos

| Arquivo | Papel |
|---|---|
| `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md` | ADR principal |
| `docs/relatorios/RELATORIO_QA_ADR-0031.md` | Relatório de QA |
| `docs/adr/INDICE_ADR.md` | Índice de ADRs |
| `docs/backlog.md` | Backlog do projeto |
| `docs/contratos/contrato_console.md` | Contrato do console |
| `docs/contratos/contrato_barra_de_menus.md` | Contrato da barra de menus |
| `docs/contratos/contrato_chip.md` | Contrato do chip |
| `docs/contratos/contrato_composicao_corpo.md` | Contrato de composição do corpo |
| `docs/contratos/contrato_json_console.md` | Contrato do JSON do console |
| `docs/contratos/contrato_tela_json.md` | Contrato do tela.json |
| `docs/nomenclatura/32_CONSOLE.md` | Módulo de nomenclatura do console |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Módulo de nomenclatura da barra e chips |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Módulo de nomenclatura de layout |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | Módulo de nomenclatura de apresentações |

---

## 4. Arquivos autorizados para alteração

| Arquivo | Status |
|---|---|
| `docs/adr/ADR-0031-*.md` | AUTORIZADO |
| `docs/adr/INDICE_ADR.md` | AUTORIZADO |
| `docs/contratos/contrato_console.md` | AUTORIZADO |
| `docs/contratos/contrato_barra_de_menus.md` | AUTORIZADO |
| `docs/contratos/contrato_chip.md` | AUTORIZADO |
| `docs/contratos/contrato_composicao_corpo.md` | AUTORIZADO |
| `docs/contratos/contrato_json_console.md` | AUTORIZADO |
| `docs/contratos/contrato_tela_json.md` | AUTORIZADO |
| `docs/nomenclatura/32_CONSOLE.md` | AUTORIZADO |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | AUTORIZADO |
| `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | AUTORIZADO |
| `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | AUTORIZADO |
| `docs/backlog.md` | AUTORIZADO |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md` | AUTORIZADO (este arquivo) |

Não autorizado: `config/`, `tela/`, `demo/`, `orquestrador.py`, `pytest.ini`,
`conftest.py`, ADR-0020 a ADR-0030, handoffs, relatórios anteriores.

---

## 5. Matriz de decisões D1–D15

| Decisão | Enunciado | Propagado para |
|---|---|---|
| **D1** | Escopo de navegação: somente console de nível único com dados já expandidos | §22.1 de `contrato_console.md`; ITEM-0007 como fronteira |
| **D2** | Elegibilidade (console focalizável): `politica_navegacao.navegavel: true` + ao menos um item com `navegavel: true` | §22.1 de `contrato_console.md`; §4.5 de `32_CONSOLE.md`; `contrato_json_console.md` nota D2 |
| **D3** | Lista de foco: travessia em profundidade da árvore de corpo; grupos são não-focalizáveis | §22.2 de `contrato_console.md`; §4.5 de `32_CONSOLE.md` |
| **D4** | Ordem espacial: irmãos em ordem da declaração JSON (esquerda→direita, cima→baixo em matrizes) | §22.2 de `contrato_console.md`; §4.5 de `32_CONSOLE.md` |
| **D5** | Tab/Shift+Tab circulares (toroidal) na lista de foco | §22.2 de `contrato_console.md` |
| **D6** | Entrada em console: sempre no item lógico 0; sem restauração de cursor anterior | §22.3 de `contrato_console.md` |
| **D7** | Ordem row-major dos itens na grade matricial: linha a linha, da esquerda para a direita | §22.4 de `contrato_console.md` |
| **D8** | Navegação toroidal por eixo: cada eixo é toróide independente | §22.4 de `contrato_console.md`; §4.5 de `32_CONSOLE.md` |
| **D9** | Célula vazia excluída do toróide; o cursor nunca entra em célula vazia | §22.4 de `contrato_console.md`; §4.3 de `32_CONSOLE.md` (nota existente, confirmada) |
| **D10** | Redistribuição e mudança de modo preservam o item lógico; somente linhas físicas são recalculadas | §22.5 de `contrato_console.md`; §4.6 de `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`; §8B de `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` |
| **D11** | Indicador de foco somente no console focado | §22.6 de `contrato_console.md` |
| **D12** | Indicador na primeira linha física do console focado; derivado do `config/estilo.json` (preset de cursor) | §22.6 de `contrato_console.md` |
| **D13** | Seleção única: item sob cursor = item selecionado; sem toggle; sem marcador de inclusão | §22.7 de `contrato_console.md` |
| **D14** | `[⇆]` aparece quando há ≥2 consoles focalizáveis; `[✥]` aparece quando console focado tem >1 item navegável (existência dinâmica de `[✥]`) | §22.8 de `contrato_console.md`; §8.3 e §20 de `contrato_barra_de_menus.md`; §8/§9/§14 de `contrato_chip.md`; §6 de `contrato_composicao_corpo.md`; §4.3/§4.4 de `31_BARRA_DE_MENUS_E_CHIPS.md` |
| **D15** | Setas restritas à página atual; paginação e demais capacidades deferidas (ITEM-0003) | §22.9 de `contrato_console.md`; §4.6 de `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` |

---

## 6. Tratamento de QA31-001

**Questão**: O relatório de QA apontou que as condições de exibição de `[⇆]` e
`[✥]` baseadas em "elementos de corpo" ou "consoles declarados navegáveis" eram
menos precisas que as condições D14 da ADR-0031 (consoles focalizáveis / console
focado com >1 item navegável).

**Decisão**: `PROPAGACAO_DOCUMENTAL` — nenhum patch na ADR-0031 é necessário.
A ADR-0031 D14 já estabelece as condições corretas. A propagação documental
consiste em atualizar os contratos e módulos de nomenclatura que ainda usavam
as condições antigas.

**Patch da ADR**: não.

**Arquivos atualizados por QA31-001**:
- `contrato_barra_de_menus.md` §8.3 e §20
- `contrato_chip.md` §8, §9, §14
- `contrato_composicao_corpo.md` §6
- `contrato_console.md` §7, §14, §22.8
- `31_BARRA_DE_MENUS_E_CHIPS.md` §4.3, §4.4

---

## 7. Tratamento de QA31-002

**Questão**: O relatório de QA identificou múltiplas ocorrências da marcação
`ADR_CREATED_AWAITING_QA` no interior da ADR-0031 (além da última linha).

**Decisão**: `PRESERVACAO_CONTEXTUAL` — as ocorrências internas são referências
históricas contextuais ao estado anterior da ADR. Não são defeitos. Apenas a
**última linha** da ADR tem papel de encerramento (encerramento substituído por
`ADR_APPLICATION_COMPLETED_AWAITING_QA`). As demais ocorrências são preservadas.

**Defeito na ADR**: não.

---

## 8. Resumo de alterações por arquivo

### 8.1 `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`

| Elemento | Antes | Depois |
|---|---|---|
| Frontmatter `status` | `ADR_CREATED_AWAITING_QA` | `aceita` |
| Seção 1 — tabela Status | `ADR_CREATED_AWAITING_QA` | `aceita` |
| Seção 2 — Status | Texto simples de criação | Bloco YAML com `status_da_adr: aceita`, `qa_da_adr`, `aplicacao_documental`, `implementacao`, `handoff` |
| Seção 20 — encerramento interno | Campos `status_da_adr: ADR_CREATED_AWAITING_QA`, `decisoes_registradas` | `status_da_adr: aceita`, `status_anterior_criacao`, `decisoes_propagadas`, campos de QA e aplicação |
| Última linha | `ADR_CREATED_AWAITING_QA` | `ADR_APPLICATION_COMPLETED_AWAITING_QA` |

### 8.2 `docs/adr/INDICE_ADR.md`

Adicionada linha de ADR-0031 na tabela de decisões registradas após ADR-0030.

### 8.3 `docs/contratos/contrato_console.md`

| Elemento | Antes | Depois |
|---|---|---|
| §7 último bullet `[⇆]` | Referência a múltiplos elementos de corpo | Referência a consoles focalizáveis e §22 |
| §14 tabela chips | Sem linha `[⇆]`; `[✥]` com condição antiga | Linha `[⇆]` adicionada; `[✥]` atualizado com D14 |
| §22 | Inexistente | Nova seção com 10 subseções (§22.1–§22.10) cobrindo D2–D15 |

### 8.4 `docs/contratos/contrato_barra_de_menus.md`

| Elemento | Antes | Depois |
|---|---|---|
| §8.3 tabela chips | `[⇆]`: "múltiplos elementos de corpo"; `[✥]`: "ao menos um console navegável" | `[⇆]`: "≥2 consoles focalizáveis (D14)"; `[✥]`: "console focado >1 item navegável (D14)" |
| §20 critérios de validação | Condições antigas para `[⇆]` e `[✥]` | Condições D14 atualizadas com referência a ADR-0031 |

### 8.5 `docs/contratos/contrato_chip.md`

| Elemento | Antes | Depois |
|---|---|---|
| Frontmatter `adrs_aplicadas` | Sem ADR-0031 | ADR-0031 adicionada |
| §8 exemplos `regra_existencia` | `tela_com_multiplos_corpos`; `tela_com_console_navegavel` | Substituídos por `tela_com_pelo_menos_dois_consoles_focalizaveis` e `console_focado_com_mais_de_um_item_navegavel`; nota sobre existência dinâmica de `[✥]` |
| §9 tabela inativo | Linha `[✥]` com condição antiga | Linha removida; nota sobre inexistência de estado inativo para `[✥]` (ADR-0031 D14) |
| §14 relação com console | "`[✥]` exige ao menos um console navegável" | Atualizado para D14: aparece dinamicamente quando console focado tem >1 item navegável |

### 8.6 `docs/contratos/contrato_composicao_corpo.md`

| Elemento | Antes | Depois |
|---|---|---|
| Frontmatter `adrs_aplicadas` | Sem ADR-0031 | ADR-0031 adicionada |
| §6 bullet `[✥]` | "inativo se elemento em foco não for console navegável" | "aparece somente quando console focado tem >1 item navegável (D14); ausente nos demais casos" |
| §6 bullet `[⇆]` | "alterna entre elementos de corpo quando há múltiplos" | "alterna entre consoles focalizáveis quando há ≥2 (D14)" |

### 8.7 `docs/contratos/contrato_json_console.md`

**Status**: INSPECIONADO_E_ATUALIZADO (referência documental).

| Elemento | Antes | Depois |
|---|---|---|
| Frontmatter `adrs_aplicadas` | Sem ADR-0031 | ADR-0031 adicionada |
| §2 descrição navegabilidade | "navegável por `[✥]` quando declara navegável e tem item navegável" | Atualizado para mencionar D2 (focalizável) e D14 (condições adicionais de `[✥]`) com remissão a `contrato_console.md` §22 |

### 8.8 `docs/contratos/contrato_tela_json.md`

**Status**: ALTERADO (esclarecimento normativo no frontmatter; sem mudança estrutural de schema).

| Elemento | Antes | Depois |
|---|---|---|
| Frontmatter `adrs_aplicadas` | Sem ADR-0031 | ADR-0031 adicionada |

Alteração documental realizada: inclusão da referência
`docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`
em `adrs_aplicadas`. O schema de `tela.json` não exigiu alteração estrutural —
D1–D15 são regras comportamentais, não mudanças de schema.

```yaml
contrato_tela_json:
  classificacao: ALTERADO
  evidencia: DIFF_MATERIAL
```

### 8.9 `docs/nomenclatura/32_CONSOLE.md`

| Elemento | Antes | Depois |
|---|---|---|
| §3 Termos proprietários | Sem terminologia de ADR-0031 | Adicionados: console focalizável/focado, item lógico/corrente, lista/ordem de foco, travessia em profundidade, navegação toroidal por eixo, linha física, coluna indicadora, seleção única |
| §4.5 | Inexistente | Nova subseção com tabela de terminologia de ADR-0031 e distinções obrigatórias adicionais |
| §5 distinções | `[✥]` × `[⇆]`: descrição antiga | Atualizado para refletir D14 |
| §7 ADRs | Sem ADR-0031 | ADR-0031 adicionada |
| §10 `adrs_relacionadas` | Sem ADR-0031 | ADR-0031 adicionada |

### 8.10 `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`

| Elemento | Antes | Depois |
|---|---|---|
| §4.3 tabela chips | `[⇆]`: `quantidade_corpos: multiplos`; `[✥]`: "ao menos um console navegável" | `[⇆]`: ≥2 consoles focalizáveis (D14); `[✥]`: console focado >1 item navegável, existência dinâmica (D14) |
| §4.4 ativo/inativo | Regra geral de inativo sem exceção | Exceção documentada para `[✥]` (existência dinâmica, ADR-0031 D14) |
| §7 ADRs | Sem ADR-0031 | ADR-0031 adicionada |
| §10 proveniência | Sem ADR-0031 | ADR-0031 adicionada |

### 8.11 `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`

| Elemento | Antes | Depois |
|---|---|---|
| §4.6 | Inexistente | Nova subseção com 3 notas de fronteira: D10 (redimensionamento preserva item lógico), D15 (setas restritas à página), ITEM-0003 (paginação deferida) |
| §7 ADRs | Sem ADR-0031 | ADR-0031 adicionada |
| §10 `adrs_relacionadas` | Sem ADR-0031 | ADR-0031 adicionada |

### 8.12 `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`

| Elemento | Antes | Depois |
|---|---|---|
| §8B | Inexistente | Nova subseção com 3 notas de fronteira: D10 (mudança de modo preserva item lógico), linhas de continuação sem indicador de cursor, navegação multinível fora de escopo (ITEM-0007) |
| §9 conteúdo que não pertence | Sem menção a ADR-0031 | Adicionado: "Navegação simples e seleção única → `contrato_console.md` §22 e módulo `32`" |
| §7 ADRs | Sem ADR-0031 | ADR-0031 adicionada |
| §10 `adrs_relacionadas` | Sem ADR-0031 | ADR-0031 adicionada |

### 8.13 `docs/backlog.md` — ITEM-0002

| Campo | Antes | Depois |
|---|---|---|
| Descrição | "consoles navegáveis" | "consoles focalizáveis" |
| Pré-requisitos | "Formalização das decisões em ADR própria" | "ADR-0031 aceita e aplicação documental aguardando QA" |
| ADR | (ausente) | `ADR-0031 (aceita)` |
| Aplicacao_documental | (ausente) | `CONCLUIDA` |
| QA_da_aplicacao | (ausente) | `PENDENTE` |
| Implementacao | (ausente) | `NAO_INICIADA` |
| Handoff | (ausente) | `NAO_CRIADO` |
| Próxima ação | "Criar a ADR especializada..." | "QA independente da aplicação documental da ADR-0031" |

---

## 9. Verificações mecânicas

### 9.1 Stage git

```
Verificação: nenhum arquivo foi adicionado ao stage durante esta aplicação.
Resultado: PASSOU
```

### 9.2 Encerramento da ADR-0031

```
Última linha de ADR-0031: ADR_APPLICATION_COMPLETED_AWAITING_QA
Resultado: PASSOU
```

### 9.3 Arquivos proibidos não alterados

```
config/: NÃO ALTERADO
tela/:   NÃO ALTERADO
demo/:   NÃO ALTERADO
orquestrador.py: NÃO ALTERADO
pytest.ini: NÃO ALTERADO
conftest.py: NÃO ALTERADO
ADR-0020 a ADR-0030: NÃO ALTERADOS
Handoffs: NÃO ALTERADOS
Relatórios anteriores: NÃO ALTERADOS
RELATORIO_QA_ADR-0031.md: NÃO ALTERADO
Resultado: PASSOU
```

### 9.4 Referências cruzadas

```
contrato_console.md §22 — referenciado por:
  - contrato_barra_de_menus.md §8.3 ✓
  - contrato_chip.md §14 ✓
  - contrato_composicao_corpo.md §6 ✓
  - 31_BARRA_DE_MENUS_E_CHIPS.md §4.3 ✓
  - 32_CONSOLE.md §4.5 ✓
ADR-0031 — referenciada por todos os contratos e módulos atualizados ✓
Resultado: PASSOU
```

### 9.5 INDICE_ADR.md

```
Linha de ADR-0031 presente com status "aceita" e data 2026-07-25.
Resultado: PASSOU
```

### 9.6 backlog.md ITEM-0002

```
Status: planejado (correto — QA da aplicação ainda pendente)
ADR: ADR-0031 (aceita)
Aplicacao_documental: CONCLUIDA
QA_da_aplicacao: PENDENTE
Implementacao: NAO_INICIADA
Handoff: NAO_CRIADO
Resultado: PASSOU
```

---

## 10. Decisões de interpretação tomadas durante a aplicação

### 10.1 Existência dinâmica de `[✥]` vs. modelo estático de `regra_existencia`

**Situação**: O contrato do chip define `regra_existencia` como estática (avaliada
na carga do `tela.json`). A condição D14 para `[✥]` ("console focado tem >1 item
navegável") é dinâmica.

**Resolução**: A aplicação documenta explicitamente a exceção. Em `contrato_chip.md`
§8 foi adicionada nota sobre existência dinâmica de `[✥]` como exceção ao modelo
geral. A regra geral permanece válida para os demais chips. Nenhuma ADR de
reconciliação do modelo genérico de existência é necessária no momento — a exceção
está documentada localmente.

### 10.2 Remoção da linha `[✥]` da tabela inativo em contrato_chip.md §9

**Situação**: A linha `[✥]` na tabela de ativo/inativo descrevia o estado inativo
do chip. Com D14, `[✥]` não tem estado inativo — está presente ou ausente.

**Resolução**: A linha foi removida da tabela. Uma nota explicativa foi adicionada
após a tabela documentando que `[✥]` não possui estado inativo (ADR-0031 D14).

### 10.3 Escopo da atualização de contrato_tela_json.md

**Situação**: O schema de `tela.json` já capturava `politica_navegacao`, `navegavel`
e `politica_selecao`. As decisões D1–D15 são regras comportamentais, não mudanças
de schema.

**Resolução**: ALTERADO. Houve diff material limitado à inclusão da referência
ADR-0031 em `adrs_aplicadas` do frontmatter (esclarecimento normativo). Classificação
anterior `INSPECIONADO_E_PRESERVADO` era factualmente incompatível com o estado
Git do arquivo e foi corrigida neste relatório como ajuste factual anterior ao QA.

```yaml
contrato_tela_json:
  classificacao: ALTERADO
  evidencia: DIFF_MATERIAL
```

---

## 11. Pendências não cobertas por esta aplicação

| Pendência | Escopo | Responsável |
|---|---|---|
| Implementação da navegação simples | Código | ITEM-0002 (aguarda QA desta aplicação + handoff) |
| Paginação interativa do console | Documentação + Implementação | ITEM-0003 |
| Seleção múltipla no console | Documentação + Implementação | ITEM-0006 |
| Navegação multinível (colapsável) | Documentação + Implementação | ITEM-0007 |
| Registry de ações (DOC-B009) | Documentação | Pendência existente |
| QA desta aplicação documental | Revisão independente | Externo |

---

## Patch posterior ao QA rejeitado

Esta seção preserva o registro histórico da aplicação inicial e qualifica seu
estado após o QA independente da aplicação.

```yaml
qa_da_aplicacao_inicial:
  relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
  classificacao: ADR_APPLICATION_QA_REJECTED

patch:
  achados_tratados:
    - QAAPP31-001
    - QAAPP31-002
    - QAAPP31-003
    - QAAPP31-004
    - QAAPP31-005
    - QAAPP31-006

  qa_pos_patch: PENDENTE

estado_processual:
  aplicacao_inicial: REJEITADA_PELO_QA
  patch_documental: CONCLUIDO
  qa_pos_patch: PENDENTE
```

As afirmações anteriores de referências cruzadas aprovadas, de reconciliação
integral de `QA31-001` e de inexistência de contradições remanescentes pertencem
ao registro da aplicação inicial. Após o relatório
`docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md`, essas afirmações ficam
qualificadas como rejeitadas pelo QA da aplicação inicial e substituídas pelo
estado processual acima. Este patch documental trata os achados `QAAPP31-001` a
`QAAPP31-006`, mas não classifica o resultado como aprovado; o QA pós-patch
permanece pendente.

ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA
