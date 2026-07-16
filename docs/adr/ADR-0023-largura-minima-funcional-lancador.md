---
name: ADR-0023-largura-minima-funcional-lancador
description: Define largura mínima funcional do lancador como coluna mínima válida; quando a área alocada fica abaixo desse limiar, o renderer aciona o quadro mínimo canônico global — a tela ou sessão TUI normal é substituída integralmente; complementa a política responsiva do H-0034 sem reabrir o H-0030
metadata:
  type: adr
  status: aceita
  data: 2026-07-15
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas:
    - QA-H0034-HANDOFF-ALTO-003
  contratos_afetados:
    - docs/contratos/contrato_lancador.md
    - docs/NOMENCLATURA.md
  handoffs_bloqueados:
    - H-0034
---

# ADR-0023 — Largura mínima funcional do `lancador`

## Status

`aceita`

## Data

2026-07-15

---

## 1. Contexto

O H-0034 especifica a distribuição responsiva do `lancador` entre os modos
`fila` e `matriz`. A regra normativa define duas etapas de decisão:

1. O renderer tenta a representação em `fila` (todos os itens em linha única).
2. Se a fila não couber, o renderer tenta a representação em `matriz`,
   maximizando colunas e iterando `n_rows` crescente até encontrar distribuição
   que caiba.

O H-0030 está fechado e esta ADR não o reabre.

Durante o QA do handoff H-0034 (`docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md`),
o achado **QA-H0034-HANDOFF-ALTO-003** identificou lacuna normativa: o handoff
define um fallback final de `n_col = 1`, `n_rows = n_itens`, mas não declara o
que acontece quando a área disponível é inferior à largura necessária para
representar integralmente essa coluna única. Sem regra explícita, o executor
precisaria escolher entre truncar, produzir overflow, omitir itens, paginar,
emitir erro ou inventar um critério de largura mínima — todos comportamentos
incompatíveis entre si e com as políticas ativas do sistema.

Esta ADR fecha essa lacuna registrando a decisão já tomada pelo usuário: a
insuficiência da área alocada ao `lancador` é condição capaz de tornar a tela
normal inutilizável, e o fallback é o quadro mínimo canônico global — não um
estado ou mensagem local restrito ao elemento.

---

## 2. Problema

O renderer do `lancador` não tem regra normativa para o caso em que:

- a representação em `fila` não cabe;
- nenhuma distribuição em `matriz` válida cabe;
- a largura útil disponível para a área do `lancador` é inferior à largura
  mínima necessária para representar integralmente uma coluna única — incluindo
  margens, vão chip↔texto e demais requisitos normativos aplicáveis.

Sem regra explícita, o executor é forçado a decidir unilateralmente entre:

- truncar textos ou chips para forçar encaixe (viola `contrato_lancador.md`
  R-3 e R-7);
- permitir overflow horizontal (viola política de alternate screen da ADR-0016);
- omitir itens (viola seção 6.1 de `contrato_lancador.md` e ADR-0001);
- paginar (viola seção 6.1 de `contrato_lancador.md`);
- emitir `RenderizadorErro` como saída normal (viola seção 9 da ADR-0017);
- impor largura mínima arbitrária sem critério aprovado.

Nenhuma dessas opções é permitida pelas políticas ativas.

---

## 3. Decisão

As declarações abaixo constituem a decisão formal desta ADR.

**3.1 Largura mínima funcional e grandezas de largura**

Esta ADR distingue quatro grandezas de largura:

- **`terminal_w`**: largura total do terminal ou viewport.

- **`area_lancador_w`**: largura total efetivamente alocada ao elemento
  `lancador` pela composição — inclui a caixa completa com bordas e padding
  externos.

- **`lancador_caixa_min_w`**: largura mínima total da caixa ou área alocada ao
  `lancador`, incluindo as unidades estruturais obrigatórias da representação
  atual (bordas e padding externos da caixa). Relação conceitual:

  ```text
  lancador_caixa_min_w = coluna_minima_content_w + largura_estrutural_da_caixa
  ```

- **`coluna_minima_content_w`**: largura mínima do conteúdo necessária para
  representar integralmente uma coluna válida, sem bordas nem padding externo
  da caixa. É a **largura mínima funcional do `lancador`**: a menor largura de
  conteúdo para a qual existe ao menos uma distribuição válida do conjunto de
  itens declarados.

A comparação normativa deve usar grandezas no mesmo domínio:

```text
content_w < coluna_minima_content_w    (domínio do conteúdo)
```

ou, equivalentemente:

```text
area_lancador_w < lancador_caixa_min_w    (domínio da caixa completa)
```

As duas formas são equivalentes quando bordas e padding da caixa são conhecidos.
Não é válido comparar diretamente `terminal_w` com `coluna_minima_content_w`,
nem comparar `area_lancador_w` com `coluna_minima_content_w` sem converter
bordas e padding.

A fórmula de `coluna_minima_content_w`:

```text
coluna_minima_content_w = vao_margem_min
                        + max_chip_sub_w + vao_chip_texto_min + max_texto_sub_w
                        + vao_margem_min
```

onde:
- `max_chip_sub_w = max(len(item["chip"]) + 2  para item em itens)`
- `max_texto_sub_w = max(len(item["texto"])     para item em itens)`
- `vao_margem_min` e `vao_chip_texto_min` vêm de `config/elementos/lancador.json`

Todos os parâmetros numéricos de vão provêm de `config/elementos/lancador.json`
sem hardcoding no renderer. Bordas e padding da caixa pertencem ao cálculo de
`lancador_caixa_min_w` e não devem ser incluídos silenciosamente em
`coluna_minima_content_w`.

**3.2 Fallback para o quadro mínimo canônico global**

Quando a área alocada ao `lancador` for insuficiente para representar
integralmente ao menos uma coluna válida, a tela normal torna-se inutilizável.
O renderer deve acionar o **quadro mínimo canônico global** (`quadro mínimo de
terminal pequeno`, definido em ADR-0017, seção 9, e registrado em
`docs/NOMENCLATURA.md`).

O quadro mínimo global **substitui integralmente toda a tela ou sessão TUI
normal**. Enquanto o quadro mínimo estiver ativo:

- o cabeçalho não é exibido;
- o corpo não é exibido;
- o `lancador` não é exibido;
- dashboards não são exibidos;
- a `barra_de_menus` não é exibida;
- nenhum outro elemento da tela normal permanece visível.

É proibido:

- renderizar mensagem dentro da caixa ou área do `lancador`;
- criar estado visual local restrito ao `lancador` ou a qualquer outro componente;
- preservar qualquer parte da tela normal enquanto o quadro mínimo estiver ativo;
- truncar textos ou chips para forçar encaixe;
- permitir overflow horizontal;
- omitir itens;
- duplicar itens;
- alterar a ordem dos itens;
- paginar o `lancador`;
- criar rolagem específica;
- escolher uma disposição geometricamente inválida;
- criar mensagem nova quando já existe o estado canônico equivalente;
- inventar variante local do aviso.

A mensagem e a apresentação seguem o mecanismo canônico já existente. Se a
redação textual do quadro mínimo não estiver fixada documentalmente, esta ADR
não define nem inventa redação nova; a futura aplicação deve reutilizar o
estado funcional existente sem criar variante local.

**3.3 Sequência normativa de decisão do renderer**

```text
obter area_lancador_w (largura total alocada ao lancador pela composição)
→ converter para content_w (descontar bordas e padding da caixa)
→ testar fila
→ testar matrizes válidas (n_rows = 2 .. n_itens, decrescente em colunas)
→ testar coluna mínima válida (n_col = 1, n_rows = n_itens)
→ se coluna mínima não couber: acionar o quadro mínimo canônico global
```

A verificação da coluna mínima não é um novo modo de layout; é o limite inferior
de validade das representações do `lancador`. O fallback final é o quadro mínimo
canônico global — não uma disposição parcial nem um estado local.

**3.4 Validade nos dois sentidos de redimensionamento**

A regra se aplica tanto na abertura da tela quanto durante qualquer
redimensionamento posterior da janela do terminal.

**3.5 Recuperação automática**

O estado de quadro mínimo não é permanente. A cada redesenho (incluindo
redesenhos provocados por `SIGWINCH`, conforme ADR-0017):

- o renderer recalcula as grandezas de largura e a sequência de decisão acima;
- se `content_w >= coluna_minima_content_w` (equivalente a
  `area_lancador_w >= lancador_caixa_min_w`), o quadro mínimo desaparece;
- a tela normal é reconstruída integralmente;
- o `lancador` volta à representação normal (fila ou matriz, conforme couber),
  recalculada a partir da largura atual;
- nenhum estado inválido do `lancador` deve permanecer visível;
- não é necessária ação do usuário para sair do estado de quadro mínimo;
- não é necessário reiniciar a aplicação;
- não há persistência do estado de quadro mínimo entre redesenhos.

---

## 4. Ordem de decisão do renderer

```text
obter area_lancador_w (largura total alocada ao lancador)
→ converter para content_w (descontar bordas e padding)
→ testar fila
→ testar matrizes válidas
→ testar coluna mínima válida
→ se a coluna mínima não couber, acionar o quadro mínimo canônico global
```

Esta ADR não define nem altera o algoritmo completo de `fila` ou `matriz`. O
único acréscimo normativo é posicionar o fallback canônico global na ordem de
decisão, após a coluna mínima.

---

## 5. Semântica do estado de quadro mínimo

### 5.1 Distinção entre situações e escopo visual

O estado canônico de `quadro mínimo de terminal pequeno` (ADR-0017) foi
originalmente definido para o caso em que as **dimensões totais do terminal**
(largura × altura) são válidas mas insuficientes para a tela normal.

Esta ADR esclarece que o mesmo estado canônico deve ser acionado quando a
**área alocada ao `lancador`** é insuficiente para representar integralmente
ao menos uma coluna válida — mesmo que a largura total do terminal seja maior,
mas a composição tenha reservado ao `lancador` uma área menor.

Em ambas as situações, o **escopo visual do fallback é idêntico e global**: o
quadro mínimo substitui toda a tela ou sessão TUI normal. Nenhum elemento da
tela normal — cabeçalho, corpo, `lancador`, dashboards, `barra_de_menus` —
permanece visível enquanto o quadro mínimo estiver ativo.

A distinção semântica entre as situações de insuficiência é:

| Situação | `terminal_w` | `area_lancador_w` | Estado resultante |
|---|---|---|---|
| Terminal fisicamente pequeno | insuficiente para a tela normal | qualquer | `quadro mínimo de terminal pequeno` (ADR-0017) — escopo global |
| Área do `lancador` insuficiente por composição | suficiente para a tela normal em outras condições | `< lancador_caixa_min_w` | mesmo estado canônico global (esta ADR) |
| Conteúdo inválido ou configuração inválida | qualquer | qualquer | `RenderizadorErro` |
| Erro de carregamento | qualquer | qualquer | mecanismo próprio de tratamento de erro |
| Ausência de itens | qualquer | qualquer | 0 linhas de conteúdo, sem erro |

A insuficiência relevante para esta ADR é aquela que torna o `lancador`
inutilizável — e, portanto, torna a tela normal inutilizável —
independentemente de a largura total do terminal ser maior. O mecanismo
canônico a ser reutilizado é o de indisponibilidade por espaço insuficiente
definido na ADR-0017, com o mesmo alcance visual global: toda a tela ou sessão
normal é substituída pelo quadro mínimo. Nenhum componente da tela normal é
preservado durante o quadro mínimo.

A recuperação ocorre pelo mecanismo reativo global já existente: a cada redesenho,
o renderer reavalia as grandezas de largura; ao recuperar
`area_lancador_w >= lancador_caixa_min_w`, o quadro mínimo desaparece e a
tela normal retorna automaticamente.

### 5.2 Mensagem canônica

A ADR-0017 não fixa o texto exato do aviso — define que deve comunicar
inequivocamente "terminal pequeno demais" e pode ser adequado à largura
disponível. `docs/NOMENCLATURA.md` registra o estado sob o nome
`quadro mínimo de terminal pequeno`.

Não existe, nesta data, uma redação canônica fixada documentalmente para o
texto da mensagem. A futura aplicação deve reutilizar o estado funcional
existente sem inventar redação nova. Se o estado já existir implementado no
renderer, deve ser reutilizado diretamente; se ainda não estiver implementado,
deve seguir a política da ADR-0017, seção 9.

Não deve ser criada mensagem específica para o `lancador` dentro de sua área
ou caixa. Qualquer texto visível nessa condição segue exclusivamente o
mecanismo canônico global.

---

## 6. Recuperação após redimensionamento

- O estado de quadro mínimo não é permanente.
- O estado global é recalculado em cada redesenho.
- A cada redesenho, o renderer avalia se `content_w >= coluna_minima_content_w`
  (equivalente a `area_lancador_w >= lancador_caixa_min_w`).
- Quando uma coluna mínima válida voltar a caber:
  - o quadro mínimo desaparece;
  - a tela normal é reconstruída integralmente;
  - o `lancador` volta ao modo normal (fila ou matriz, conforme couber);
  - a redistribuição do `lancador` é recalculada integralmente entre `fila` e
    `matriz` a partir da largura atual.
- Nenhum item omitido deve persistir após a recuperação.
- Não há truncamento, overflow, paginação, omissão ou perda de itens.
- Nenhum estado inválido do `lancador` deve permanecer visível.
- Não é necessária ação do usuário.
- Não é necessário reiniciar a aplicação.
- Não há persistência do estado de quadro mínimo.

---

## 7. Compatibilidade

Esta decisão:

- não altera o limite de 15 caracteres dos textos de itens;
- não altera chips, ações ou destinos;
- não cria paginação;
- não cria truncamento;
- não cria reticências ou overflow;
- não cria quebra de linha para itens;
- não cria rolagem;
- não cria navegação ou seleção específica;
- não cria mensagem nova específica para o `lancador`;
- não cria variante local do aviso dentro da área ou caixa do `lancador`;
- não cria novo estado visual local restrito ao `lancador`;
- não cria novo tipo de componente;
- não altera a `barra_de_menus`;
- não altera o cabeçalho;
- não altera `destino_minimo` ou `grupo_minimo`;
- não reabre o H-0030;
- não inicia o H-0033;
- complementa a política responsiva do `lancador` definida pelo H-0034.

---

## 8. Consequências

### Obrigatórias

- O `contrato_lancador.md` deve receber seção normativa declarando a
  `largura_minima_funcional_lancador`, as grandezas de largura e o fallback
  para o quadro mínimo canônico global.
- Se `largura_minima_funcional_lancador` for introduzido como termo normativo
  novo, `docs/NOMENCLATURA.md` deve registrá-lo.
- O handoff H-0034 precisa de atualização (via `PATCH_HANDOFF`, ver seção 9)
  para declarar o comportamento quando `content_w < coluna_minima_content_w`.
- A futura implementação deve incluir testes de fronteira para o limiar
  `coluna_minima_content_w` (um caractere acima = renderização normal; um
  caractere abaixo = quadro mínimo canônico global).
- A futura implementação deve incluir teste de recuperação: ampliar a largura
  a partir do estado canônico global deve restaurar a tela normal
  automaticamente, sem reinicialização.
- A validação manual em TTY real é possível e recomendada, mas não é bloqueante
  para aprovação dos testes automatizados.
- O truncamento silencioso não pode ser aprovado em nenhuma circunstância;
  a ausência de teste de largura mínima não implica permissão para truncar.

---

## 9. Documentos afetados

### Documentos que devem ser atualizados na futura etapa `APLICAR_ADR`

```yaml
- documento: docs/contratos/contrato_lancador.md
  afetado: sim
  justificativa: |
    Não declara largura_minima_funcional_lancador, as grandezas de largura
    (coluna_minima_content_w, lancador_caixa_min_w, area_lancador_w, terminal_w)
    nem o fallback para o quadro mínimo canônico global. Deve receber seção
    normativa com: definição das grandezas e suas relações, sequência de decisão
    com fallback canônico global, proibições de fallback local e regra de
    recuperação automática.
  conteudo_a_propagar: |
    Definição de coluna_minima_content_w, lancador_caixa_min_w, area_lancador_w
    e terminal_w. Sequência normativa: obter area_lancador_w → converter para
    content_w → fila → matrizes → coluna mínima → quadro mínimo global.
    Proibições: fallback local, truncamento, overflow, omissão, paginação.
    Regra de recuperação automática global.

- documento: docs/NOMENCLATURA.md
  afetado: sim
  justificativa: |
    Deve registrar largura_minima_funcional_lancador (ou coluna_minima_content_w)
    como termo normativo, caso introduzido como tal; e complementar a seção
    relativa ao tipo lancador com a regra de fallback canônico global e as
    grandezas de largura.
  conteudo_a_propagar: |
    Termos normativos: largura_minima_funcional_lancador, coluna_minima_content_w,
    lancador_caixa_min_w, area_lancador_w. Regra de fallback global quando
    nenhuma coluna válida couber.

- documento: docs/adr/INDICE_ADR.md
  afetado: sim
  justificativa: |
    Todo registro de ADR aprovada exige entrada no índice.
  conteudo_a_propagar: |
    Entrada de ADR-0023 com status aceita, data 2026-07-15 e resumo da decisão.

- documento: docs/contratos/contrato_tela_json.md
  afetado: sim
  justificativa: |
    A seção 24 (redimensionamento reativo, ADR-0017) define o gatilho do quadro
    mínimo como "dimensões válidas mas insuficientes para a tela normal" —
    trata apenas insuficiência das dimensões totais do terminal. Esta ADR estende
    o gatilho para a insuficiência da área interna alocada ao lancador. A redação
    atual não cobre esse caso: menciona dimensões do terminal, não impossibilidade
    de renderização por área de componente interno. A seção 24 precisa ser
    complementada para reconhecer que a impossibilidade de representar o lancador
    em ao menos uma coluna válida também aciona o quadro mínimo canônico global,
    com o mesmo alcance visual: toda a tela normal é substituída.
  conteudo_a_propagar: |
    Complemento à seção 24: além da insuficiência das dimensões totais do
    terminal, a insuficiência da area_lancador_w para comportar ao menos uma
    coluna válida (area_lancador_w < lancador_caixa_min_w) é gatilho independente
    do mesmo quadro mínimo canônico global. O escopo visual é idêntico: toda a
    tela normal é substituída. A recuperação ocorre pelo mesmo mecanismo reativo.

- documento: docs/contratos/contrato_composicao_corpo.md
  afetado: sim
  justificativa: |
    A seção 5.10 (terminal pequeno demais, ADR-0017) restringe o gatilho do
    quadro mínimo a "dimensões válidas mas insuficientes para a tela normal".
    A seção 5.21 (terminal e área insuficiente em matriz) cita "quadro global de
    terminal pequeno" mas o restringe às "regras globais existentes (ADR-0017)"
    sem contemplar o gatilho por área interna de componente. Nenhuma das seções
    existentes reconhece que a insuficiência de area_lancador_w pode acionar o
    quadro mínimo global independentemente das dimensões totais do terminal.
    A seção 5.10 precisa ser complementada.
  conteudo_a_propagar: |
    Complemento à seção 5.10: a insuficiência da area_lancador_w para comportar
    ao menos uma coluna válida (area_lancador_w < lancador_caixa_min_w) constitui
    gatilho do quadro mínimo canônico global, com o mesmo alcance visual da
    ADR-0017 — toda a tela normal substituída. A recuperação ocorre pelo mesmo
    mecanismo reativo global.
```

### Documentos avaliados e não afetados na etapa `APLICAR_ADR`

```yaml
- documento: docs/contratos/contrato_json_lancador.md
  afetado: nao
  justificativa: |
    Não declara regras de layout ou cálculo de largura — especifica apenas a
    forma mínima do JSON de instância. Não requer atualização por esta ADR.
```

### Separação processual: H-0034

O handoff `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
precisa de atualização para incorporar a regra desta ADR, especificamente:

- a declaração das grandezas de largura (`coluna_minima_content_w`,
  `lancador_caixa_min_w`, `area_lancador_w`) na seção 3.4;
- o fallback canônico global na sequência de decisão;
- o critério de largura inferior ao mínimo de coluna como condição para o
  estado canônico global.

Entretanto, o processo vigente (`contrato_processo_desenvolvimento.md`)
classifica essa correção como `PATCH_HANDOFF`, não como `APLICAR_ADR`. A
etapa `APLICAR_ADR` não deve corrigir o handoff H-0034 diretamente. A
correção do handoff deve ocorrer em ciclo próprio de `PATCH_HANDOFF` após
a `APLICAR_ADR` ter sido concluída.

---

## 10. Critérios para futura aplicação

A aplicação desta ADR deverá tornar verificável que:

1. Existe uma definição normativa de `coluna_minima_content_w` e
   `lancador_caixa_min_w` em `contrato_lancador.md`, com as relações entre as
   quatro grandezas de largura (`terminal_w`, `area_lancador_w`,
   `lancador_caixa_min_w`, `coluna_minima_content_w`).
2. O fallback ocorre somente quando nenhuma representação válida cabe — fila,
   nenhuma matriz, e nem a coluna mínima.
3. O estado canônico existente (`quadro mínimo de terminal pequeno`, ADR-0017)
   é reutilizado com escopo **global**: toda a tela normal é substituída; não
   é criado estado paralelo nem variante local.
4. Nenhum elemento da tela normal — cabeçalho, corpo, `lancador`, dashboards,
   `barra_de_menus` — é exibido enquanto o quadro mínimo estiver ativo.
5. Não há truncamento silencioso: o renderer não abrevia chip nem texto para
   forçar encaixe.
6. Não há overflow horizontal: o renderer não escreve além de `content_w`.
7. Não há paginação: o `lancador` não divide seus itens em páginas.
8. Nenhum item é perdido, duplicado ou reordenado.
9. A recuperação por ampliação é automática: ampliar `area_lancador_w` acima
   de `lancador_caixa_min_w` restaura a tela normal sem ação do usuário e sem
   reinicialização.
10. Os contratos não contradizem a regra: `contrato_lancador.md`,
    `contrato_tela_json.md` e `contrato_composicao_corpo.md` devem ser
    consistentes com esta ADR após `APLICAR_ADR`.
11. O H-0034 pode ser corrigido por `PATCH_HANDOFF` sem nova decisão
    arquitetural, porque a decisão foi registrada aqui.
12. A comparação normativa usa grandezas no mesmo domínio: `content_w` contra
    `coluna_minima_content_w`, ou `area_lancador_w` contra
    `lancador_caixa_min_w`; nunca `terminal_w` contra `coluna_minima_content_w`.

---

## 11. Relação com ADRs anteriores

| ADR | Relação |
|---|---|
| **ADR-0001** (`menu` suporta matriz) | Origem histórica da regra de fila/matriz para o `lancador` (então `menu`). Esta ADR complementa, sem substituir. |
| **ADR-0002** (`menu` usa sobra à direita) | Regra de alinhamento horizontal. Não é alterada. |
| **ADR-0003** (vãos elásticos do `menu`) | Parâmetros de vão usados na fórmula de `coluna_minima_content_w`. Não é alterada. |
| **ADR-0013** (ocupação vertical da janela) | Normatizou `altura_disponivel` como dimensão explícita. Não é alterada; não há relação direta com largura mínima. |
| **ADR-0016** (execução em tela cheia TTY) | Proíbe overflow e scroll; o quadro mínimo canônico global deve respeitá-la. Não é alterada. |
| **ADR-0017** (redimensionamento reativo da TUI) | **Autoridade primária** do estado canônico reutilizado. Define `quadro mínimo de terminal pequeno`, recuperação automática e proibição de encerrar sessão. Esta ADR estende o gatilho desse estado para insuficiência da área alocada ao `lancador`, mantendo o mesmo escopo visual global: toda a tela ou sessão normal é substituída pelo quadro mínimo — não apenas a área do componente. Não substitui ADR-0017. |

Não há evidência de ADR anterior que defina largura mínima funcional do
`lancador` como conceito próprio. Não existe substituição de ADR anterior.

---

## 12. Itens fora de escopo desta ADR

Estão expressamente fora do escopo desta ADR:

- Algoritmo completo de cálculo de fila e matriz (definido no H-0034).
- Escolha dos vãos entre itens e colunas (definida em ADR-0003 e
  `config/elementos/lancador.json`).
- Mudança dos textos dos itens.
- Truncamento com reticências.
- Quebra de linhas dos itens.
- Paginação do `lancador`.
- Rolagem do `lancador`.
- Navegação entre itens do `lancador`.
- Seleção de itens.
- Execução de ações.
- Persistência de estado.
- Alteração da `barra_de_menus`.
- Regras do cabeçalho.
- Implementação do código.
- QA da implementação.
- Commit.

---

## Fora do escopo desta ADR

Nenhuma decisão nova foi criada além do comportamento de fallback descrito.
A regra normativa de fila/matriz já estava autorizada pelas autoridades ativas.
Esta ADR apenas fecha a lacuna de comportamento quando nenhuma disposição válida
cabe na largura disponível.
