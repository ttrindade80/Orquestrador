---
name: contrato-console
description: Schema e regras do console como container genérico de itens heterogêneos, declarado no tela.json — navegação por item, seleção por política, ação de Enter por item, modo normal/verboso e paginação após filtros
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - "docs/NOMENCLATURA.md#4-corpo-tipo-console"
      - "docs/adr/ADR-0008-modelo-configuracao-por-tela.md"
      - "docs/contratos/contrato_tela_json.md"
      - "docs/contratos/contrato_composicao_corpo.md"
    adrs_aplicadas:
      - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
      - docs/adr/ADR-0006-renomeacao-console-dashboard.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    reaproveitado_de_legado: false
---

# Contrato — `console`

## 1. Objetivo

Definir o `console` como container genérico de itens heterogêneos, declarado
no `tela.json`. Este contrato fecha a natureza do tipo, a estrutura mínima de
uma instância, a definição de itens internos, as políticas de composição,
navegação, seleção, modo verboso, paginação, colunas e filtros, e os critérios
de validação.

Este contrato não implementa código, não cria JSON real de tela e não fecha
os contratos específicos dos tipos internos de item nem o registry completo
de ações.

---

## 2. Natureza do `console`

`console` é um elemento de corpo interativo e navegável, declarado no
`tela.json`. É um **container genérico**: pode conter itens de tipos
diferentes — não presume homogeneidade de conteúdo.

Propriedades fundamentais:

- `console` é **container genérico** — não mapeia para um único tipo de dado
  ou uma única estrutura interna fixa;
- `console` pode conter **itens heterogêneos** — itens de tipos diferentes
  coexistem na mesma instância;
- `console` **não é sinônimo de tela** — é um elemento de corpo, um dos
  possíveis integrantes de `corpo.elementos[]`;
- `console` **não é `lancador`** — `lancador` aciona navegação para outras
  telas; `console` é container interativo de dados ou saída;
- `console` **não é `dashboard`** — `dashboard` é saída passiva não
  navegável; `console` é interativo e navegável por `[✥]`;
- `console` **não é `barra_de_menus`** — `barra_de_menus` é região fixa da
  tela, externa ao corpo;
- a **instância concreta** do `console` vem do `tela.json` — não de JSON
  global por domínio;
- o **renderer executa a declaração validada** — não decide composição,
  itens, filtros, paginação, colunas, ações ou navegação por conta própria.

| Conceito | O que é |
|---|---|
| Tipo `console` | Conjunto de regras, invariantes e comportamento mínimo — definido por este contrato |
| Instância de `console` | Elemento declarado em `corpo.elementos[]` no `tela.json` de uma tela; contém política de composição, navegação, seleção, itens ou binding de itens |

---

## 3. Estrutura mínima da instância

Uma instância de `console` no `tela.json` deve declarar, no mínimo:

```text
id
tipo = console
titulo ou identificador visual
origem_dados ou binding
itens ou regra de geração de itens
politica_composicao
politica_navegacao
politica_selecao
politica_paginacao
politica_exibicao
```

Semântica de cada campo:

| Campo | Descrição |
|---|---|
| `id` | Identificador estável e único do elemento no escopo do `tela.json`. Obrigatório. Usado para validação, binding, diagnóstico e manutenção. |
| `tipo` | Deve ser o valor literal `console`. Obrigatório. |
| `titulo` | Identificador visual da instância — rótulo exibido na borda ou no cabeçalho do elemento. Pode ser omitido se a instância não exibir título, desde que haja outra forma de identificação no contexto. |
| `origem_dados` ou `binding` | Fonte dos dados que alimentam os itens do `console`. Pode ser um binding declarativo ou uma referência a uma origem de dados registrada. Instância sem origem de dados, binding ou regra de geração de itens é inválida. |
| `itens` ou regra de geração de itens | Lista de itens declarados ou regra de binding que gera a lista dinamicamente a partir da origem de dados. |
| `politica_composicao` | Define como os itens são organizados visualmente — alinhamento, fluxo, espaçamento e regras de overflow. Ver seção 5. |
| `politica_navegacao` | Define se o `console` é navegável, como o cursor se move entre itens e o comportamento de wrap. Ver seção 7. |
| `politica_selecao` | Define a política de seleção: `nenhuma`, `unica` ou `multipla`. Ver seção 8. |
| `politica_paginacao` | Define se a instância pagina, o que ocorre quando o conteúdo não cabe e como os chips `[<][>]` são acionados. Ver seção 12. |
| `politica_exibicao` | Define se a instância aceita modo verboso, qual é o modo inicial e as regras de overflow em modo normal. Ver seção 6. |

---

## 4. Itens internos heterogêneos

O `console` pode conter itens internos de tipos diferentes. Cada item é
uma entidade declarativa com identidade, tipo, binding, comportamento de
navegação e ação próprios.

Campos que cada item pode declarar:

```text
id
tipo
binding
renderizador
navegavel
selecionavel
acao_enter
politica_quebra
politica_exibicao
```

Semântica de cada campo:

| Campo | Descrição |
|---|---|
| `id` | Identificador estável e único do item no escopo da instância. Obrigatório. |
| `tipo` | Tipo do item — determina o contrato de renderização e os campos esperados. Tipo desconhecido é erro de validação. |
| `binding` | Vínculo entre dados e campos exibidos pelo item. |
| `renderizador` | Identificador do renderizador responsável por este tipo de item. Permite ao renderer delegar a renderização específica sem hardcodar. |
| `navegavel` | `true` \| `false`. Determina se o cursor do `console` pode entrar neste item. Item com `navegavel: false` é ignorado pelo ciclo de navegação. |
| `selecionavel` | `true` \| `false`. Determina se este item participa do toggle de seleção `[␣]`. Só relevante quando `politica_selecao = multipla`. |
| `acao_enter` | Ação declarada e registrada que é executada quando `[⏎]` é acionado com este item em foco. Ausência significa que `[⏎]` fica inativo ao focar este item. |
| `politica_quebra` | Define o comportamento de quebra de página: `evitar_quebra`, `permitir_quebra` ou `permitir_quebra_somente_se_maior_que_pagina`. Ver seção 12. |
| `politica_exibicao` | Regras internas de renderização do item em modo normal e verboso. |

Regras dos itens internos:

- o **cursor navega por item**, não por linha física — um item pode ocupar uma
  ou mais linhas, e o cursor se move de item a item;
- itens diferentes podem ter ações diferentes no mesmo `console`;
- item sem `acao_enter` válida torna `[⏎]` **inativo** enquanto esse item
  estiver em foco;
- item com `acao_enter` válida torna `[⏎]` **ativo** enquanto estiver em foco;
- item com `navegavel: false` **não entra no ciclo de navegação** — o cursor
  o ignora ao avançar ou recuar;
- item com `selecionavel: false` **não participa do toggle** `[␣]`;
- contratos próprios de tipos internos específicos de item podem ser criados
  futuramente (pendência DOC-B008).

---

## 5. Política de composição

A política geral de composição pertence à instância do `console`, declarada
no `tela.json`. O renderer encaixa o resultado renderizado de cada item
dentro desta política — sem deliberar composição fora dela.

Aspectos cobertos:

| Aspecto | Descrição |
|---|---|
| `alinhamento` / `origem_visual` | Regra de alinhamento do bloco de itens na área disponível — ex.: centralizado, à esquerda com sobra à direita. |
| Linha por item em modo normal | Em modo normal, cada item tipicamente ocupa uma linha quando seu conteúdo cabe. O `console` não pressupõe multilinhas por item em modo normal, salvo política declarada. |
| Truncamento com reticências | Em modo normal, conteúdo que excede a largura disponível é truncado com `...` conforme política de overflow da instância. |
| Expansão vertical em modo verboso | Em modo verboso, itens podem se expandir para múltiplas linhas para exibir o conteúdo integral. |
| Separação entre política geral e renderização específica | A política do `console` define o envelope; cada item define como preenche esse envelope. O renderer não mistura as duas camadas. |
| Proibição de composição hardcoded | O renderer não decide composição fora da política declarada na instância. |

Exemplo conceitual de composição em modo normal (não é layout universal
obrigatório):

```text
     KEY
     NOME: valor longo do segundo item que estoura linha...
```

Este exemplo ilustra truncamento com reticências e alinhamento de rótulo/valor.
Não impõe que toda instância de `console` use este formato — a instância
declara sua própria política.

---

## 6. Modo normal e modo verboso

| Modo | Descrição |
|---|---|
| Normal | Compacto. Cada item renderiza na largura disponível. Conteúdo que excede pode ser truncado com `...` conforme `politica_exibicao` da instância. |
| Verboso | Expansivo. Itens podem se expandir verticalmente para exibir o conteúdo integral. O número de linhas por item pode crescer. |

Regras:

- **modo normal é o default** — instância sem declaração explícita de modo
  inicia em normal;
- modo normal **pode truncar** conteúdo com `...` conforme a `politica_exibicao`
  declarada pela instância;
- modo verboso **permite expansão vertical** dos itens;
- `[V]` **alterna modo verboso** quando a instância declara que aceita modo
  verboso — se a instância não permitir, o chip `[V]` não existe;
- modo verboso é **estado de exibição reutilizável** — não é variação
  específica de cada tela, e o renderer não hardcoda comportamento de modo
  verboso por tela;
- cada tipo de item decide **como expandir** em modo verboso, dentro da
  política geral da instância;
- a transição entre modos não altera o cursor, a seleção nem os filtros ativos.

---

## 7. Navegação

O `console` é navegável por `[✥]` (setas do teclado) quando a instância
declara navegação habilitada e há ao menos um item com `navegavel: true`.

Regras:

- a **navegação ocorre por item navegável**, nunca por linha física do terminal;
- `[✥]` representa a dica visual de "use as setas do teclado" — as setas
  físicas executam o movimento;
- `[✥]` **não navega `lancador`** (ADR-0005);
- `[✥]` **não navega `dashboard`** — `dashboard` é saída passiva;
- itens com `navegavel: false` são **ignorados** pelo cursor ao avançar ou
  recuar;
- se **não houver item navegável** na instância, o chip `[✥]` deve ser
  inexistente ou ficar inativo conforme a `regra_existencia` e `regra_ativo`
  declaradas para o chip na `barra_de_menus`;
- o comportamento de wrap toroidal (fechamento de bordas) é governado pela
  `politica_navegacao` da instância;
- quando há múltiplos elementos de corpo, `[⇆]` alterna o foco entre eles e
  `[✥]` navega dentro do elemento em foco.

---

## 8. Seleção

A política de seleção é declarada pela instância de `console` no `tela.json`:

```text
nenhuma
unica
multipla
```

Regras por política:

| Política | Descrição |
|---|---|
| `nenhuma` | Não há seleção. `[␣]` não existe nesta instância. Itens com `selecionavel: true` declarado são inconsistência de validação. |
| `unica` | O cursor define o item alvo. Não há toggle. `[␣]` não existe. O item em foco é o alvo implícito de `[⏎]`. |
| `multipla` | `[␣]` alterna a seleção do item em foco. Somente itens com `selecionavel: true` participam do toggle. Itens com `selecionavel: false` não mudam de estado ao acionar `[␣]`. |

Regras complementares:

- item precisa declarar `selecionavel: true` para participar do toggle;
- item com `selecionavel: false` não muda de estado quando `[␣]` é acionado;
- **seleção é estado de runtime** — não pertence ao JSON; não é armazenada no
  `tela.json` como estado vivo;
- `[esc]` limpa a seleção ativa quando há seleção (ver `contrato_barra_de_menus.md`
  seção 9);
- seleção persiste entre páginas quando o `console` pagina.

---

## 9. Enter / ação do item em foco

`[⏎]` executa a ação do item **em foco** no momento do acionamento.

Regras:

- a ação pertence ao **item** ou ao **binding do item** — não à tela de forma
  monolítica;
- itens diferentes na mesma instância podem ter **ações diferentes**;
- item **sem `acao_enter` válida** torna `[⏎]` **inativo** enquanto esse item
  estiver em foco;
- item **com `acao_enter` válida** torna `[⏎]` **ativo** enquanto estiver em
  foco;
- a ação deve ser **declarativa e registrada/whitelisted** no registro de ações
  do `tela.json` — comando arbitrário é proibido;
- o renderer recalcula o estado de `[⏎]` a cada render com base no item em
  foco — não guarda estado entre renders.

---

## 10. Ctrl+C em execução interna (ADR-0016)

`ISIG` permanece habilitado na sessão TUI. Durante execução futura de script
ou processo interno disparado pela aplicação a partir de ação registrada do
`console`, `KeyboardInterrupt` deve ser capturado no escopo dessa chamada e
interromper somente essa execução; a sessão TUI deve permanecer ativa.

Fora desse escopo de execução interna, `KeyboardInterrupt` deve ser ignorado
silenciosamente. Esc continua sendo a única saída normatizada da sessão TUI.
O mecanismo pode existir antes de haver fluxo real de execução interna, mas
não deve ser criada execução de script apenas para consumi-lo.

Esta regra é uma política de comportamento de execução. Ela não transfere para
este contrato as regras de renderização terminal, escape codes, buffer,
refresh, alternate screen, autowrap ou desenho de quadro da ADR-0016.

---

## 11. Filtros

Filtros reduzem o conjunto de itens exibidos antes da paginação.

Regras:

- filtros são **declarados no `tela.json`** — não hardcoded no renderer;
- filtros podem ser **refletidos por chips** da `barra_de_menus` (tipo `filtro`
  ou `alternancia`, declarados na instância da barra);
- filtros **atuam sobre dados vinculados** ao `console` pela `origem_dados` ou
  `binding`;
- filtros são **aplicados antes da paginação** — o conjunto paginado é sempre
  o resultado filtrado;
- adicionar filtro sobre atributo já existente nos dados deve ser **alteração
  declarativa no JSON da tela** — não exige alteração de código de
  renderização;
- filtro que referencia campo inexistente nos dados vinculados é **inválido**;
- o renderer não pode conter lógica hardcoded de filtro específico — toda
  lógica de filtro é derivada da declaração no `tela.json`.

---

## 12. Paginação

Paginação é consequência automática do conteúdo renderizado que não cabe na
área disponível.

Regras:

- filtros são **aplicados antes** da paginação;
- **modo normal/verboso altera** o número de linhas por item e, portanto, o
  número de itens por página;
- cada item pode declarar **política de quebra de página**:

| Política de quebra | Descrição |
|---|---|
| `evitar_quebra` | O item deve ser movido inteiro para a próxima página quando possível. Se o item não couber inteiro nem em página vazia, a quebra passa a ser permitida. |
| `permitir_quebra` | O item pode atravessar páginas normalmente. |
| `permitir_quebra_somente_se_maior_que_pagina` | O item evita quebra, salvo quando não cabe nem em página vazia. |

- chips `[<][>]` **refletem o estado de paginação** — existem quando a
  instância declara `paginacao: com`; ficam inativos quando há apenas uma
  página;
- **página atual é estado de runtime** — não pertence ao JSON; não é
  armazenada no `tela.json` como estado vivo;
- seleção persiste entre páginas.

---

## 13. Colunas

A quantidade de colunas é uma política declarada pela instância.

Regras:

- `[-][+]` **só existe** quando a instância de `console` declara
  `colunas_ajustavel: com`;
- **ajuste de coluna é estado de runtime** — não pertence ao JSON;
- quando `colunas_ajustavel: com`, a instância deve declarar o **número
  mínimo** (geralmente 1) e o **número máximo** (calculado pelo renderer a
  partir da largura atual do terminal);
- o renderer não decide sozinho a quantidade de colunas fora da política
  declarada — nem aumenta nem reduz colunas por conta própria;
- `n_col` não aparece dentro do chip `[-][+]` — o chip exibe apenas o rótulo
  de "Colunas" (decisão intencional de design).

---

## 14. Relação com `chip` e `barra_de_menus`

O `console` **não desenha** a `barra_de_menus`. A `barra_de_menus` é uma
região fixa da tela, declarada separadamente no `tela.json`.

O `console` **expõe capacidades e estado** que os chips da `barra_de_menus`
podem refletir. A `barra_de_menus` é espelho da declaração — não fonte de
decisão.

| Chip (notação documental) | Dependência do `console` |
|---|---|
| `[✥]` | Existe quando a tela possui ao menos um `console` navegável; ativo quando o `console` navegável está em foco |
| `[␣]` | Existe quando a instância de `console` declara seleção múltipla |
| `[⏎]` | Ativo quando o item em foco tem `acao_enter` válida; inativo caso contrário |
| `[V]` | Existe quando a instância de `console` declara que permite modo verboso |
| `[<][>]` | Existe quando a instância de `console` declara `paginacao: com` |
| `[-][+]` | Existe quando a instância de `console` declara `colunas_ajustavel: com` |

Chips continuam sendo **entidades da `barra_de_menus`** — não do `console`.
O `console` não cria, não ordena e não distribui chips.

---

## 15. Relação com `dashboard` e `lancador`

- `console` pode **coexistir com `dashboard`** no corpo quando o `tela.json`
  assim declara;
- `console` pode **coexistir com `lancador`** somente se a composição da tela
  declarar ambos em `corpo.elementos[]`;
- `dashboard` é **passivo e não navegável** por `[✥]` — não interfere no
  cursor do `console`;
- `lancador` é **acionado diretamente** por seus próprios itens via
  `tela_destino` — não é navegável por `[✥]`;
- regras de navegação do `console` (cursor, wrap, páginas) **não contaminam**
  `lancador` nem `dashboard`;
- quando há múltiplos elementos de corpo, `[⇆]` alterna o foco entre eles —
  o `console` só é navegável por `[✥]` quando está em foco.

---

## 16. Regras de uso

**R-1. Instância obrigatoriamente declarada no `tela.json`.**
Nenhum `console` existe sem declaração em `corpo.elementos[]` do `tela.json`.
O renderer não cria `console` por default nem por fallback.

**R-2. Renderer como executor puro.**
O renderer recebe a declaração validada e a executa. Não decide composição,
filtros, paginação, colunas, ações, itens nem navegação fora da política
declarada na instância.

**R-3. Navegação por item, nunca por linha física.**
O cursor do `console` se move de item navegável a item navegável. Linhas
físicas do terminal não são unidade de navegação.

**R-4. Filtros sempre antes da paginação.**
O conjunto paginado é sempre o resultado do filtro ativo. Nenhum renderer
pode paginar antes de filtrar.

**R-5. Ação pertence ao item, não à tela.**
`[⏎]` executa a ação do item em foco. O renderer recalcula o estado de
`[⏎]` a cada render. Não guarda estado de ação entre renders.

**R-6. Seleção, paginação e modo verboso são estado de runtime.**
Nenhum desses valores é armazenado no `tela.json` como estado vivo. O JSON
pode declarar defaults iniciais; o estado pertence à execução.

**R-7. Proibição de hardcoding.**
Nenhum item, filtro, ação, política de paginação, regra de coluna, regra de
navegação nem regra de composição pode estar hardcoded no código. O renderer
percorre as listas e objetos declarados no `tela.json`.

**R-8. Ações declarativas e whitelisted.**
Toda `acao_enter` de item deve pertencer ao registro de ações conhecidas.
Comando arbitrário é proibido.

---

## 17. Critérios de validação

- [ ] Instância de `console` sem `id` é inválida.
- [ ] Instância de `console` sem `tipo` é inválida.
- [ ] Instância de `console` com `tipo` diferente de `console` é inválida para
      este contrato.
- [ ] Instância de `console` sem `titulo` ou identificador visual é inválida.
- [ ] Instância de `console` sem `origem_dados`, `binding` ou regra de geração
      de itens é inválida.
- [ ] Instância de `console` sem `politica_composicao` é inválida.
- [ ] Instância de `console` sem `politica_navegacao` é inválida.
- [ ] Instância de `console` sem `politica_selecao` é inválida.
- [ ] Instância de `console` sem `politica_paginacao` é inválida.
- [ ] Instância de `console` sem `politica_exibicao` é inválida.
- [ ] Item sem `id` é inválido.
- [ ] Item sem `tipo` é inválido.
- [ ] Item com tipo desconhecido pelo renderer é inválido.
- [ ] Item com `navegavel: true` sem estrutura suficiente para foco é inválido.
- [ ] Item com `selecionavel: true` em instância com `politica_selecao = nenhuma`
      é inconsistência de validação.
- [ ] Seleção múltipla sem ao menos um item com `selecionavel: true` torna
      `[␣]` inválido ou inexistente.
- [ ] `acao_enter` não registrada no whitelist é inválida.
- [ ] Filtro que referencia campo inexistente nos dados vinculados é inválido.
- [ ] Instância com `paginacao: com` sem `politica_paginacao` declarada é
      inválida.
- [ ] Política de quebra desconhecida em item é inválida.
- [ ] O renderer não pode hardcodar item, filtro, ação, paginação, coluna,
      navegação nem composição.
- [ ] `[✥]` não pode ser vinculado a `lancador` nem a `dashboard` como condição
      de existência (ADR-0005).
- [ ] `[␣]` não pode existir se a instância não declara `politica_selecao =
      multipla`.
- [ ] Filtros são aplicados antes da paginação — qualquer implementação que
      inverta a ordem é violação contratual.

---

## 18. Pendências fora de escopo

Os itens abaixo estão fora do escopo deste contrato:

- **Contratos específicos dos tipos internos de item** (DOC-B008): cada tipo
  interno de item pode ter contrato próprio com campos, renderização normal/
  verbosa, quebra de página, navegabilidade e selecionabilidade próprios.
- **Registry completo de ações** (DOC-B009): os tipos de `acao_enter`
  declaráveis e seus parâmetros formam um registry a ser definido em tarefa
  própria.
- **Implementação do cursor**: mecanismo de navegação interna, posição
  corrente, wrap toroidal detalhado e tratamento de célula vazia pertencem
  à implementação futura.
- **Implementação de paginação**: algoritmo de quebra, cálculo de páginas,
  buffer de renderização.
- **Implementação de filtros**: lógica de execução do filtro sobre os dados
  vinculados.
- **JSON real da tela raiz do Orquestrador** (DOC-B011): a criação do primeiro
  JSON real de tela aguarda DOC-B010.
- **Testes automatizados**: critérios de validação deste contrato são
  verificáveis, mas testes não são parte deste artefato documental.
- **Renderização final em terminal**: caracteres, cores, escape codes e
  chamadas de sistema não pertencem a este contrato.
- **Decisões de performance**: buffer, refresh parcial, debounce de input e
  similares pertencem à implementação.
