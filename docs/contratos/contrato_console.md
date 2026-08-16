---
name: contrato-console
description: Schema e regras do console como container genérico de itens heterogêneos, declarado no tela.json — navegação por item, seleção por política, ação de Enter por item, modo normal/verboso e paginação após filtros
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.2"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - "docs/nomenclatura/32_CONSOLE.md"
      - "docs/adr/ADR-0008-modelo-configuracao-por-tela.md"
      - "docs/contratos/contrato_tela_json.md"
      - "docs/contratos/contrato_composicao_corpo.md"
    adrs_aplicadas:
      - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
      - docs/adr/ADR-0006-renomeacao-console-dashboard.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
      - docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
      - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
      - docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md
      - docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
      - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
      - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
      - docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
      - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
      - docs/adr/ADR-0042-navegacao-multinivel-do-console.md
    reaproveitado_de_legado: false
  dependencias_nomenclatura:
    dependencias_obrigatorias:
      - docs/nomenclatura/01_NUCLEO_COMUM.md
      - docs/nomenclatura/32_CONSOLE.md
    dependencias_condicionais:
      - modulo: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
        quando: tratar chips de navegação, seleção ou filtro
      - modulo: docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
        quando: tratar conteúdo externo recebido pelo console
      - modulo: docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
        quando: tratar carregamento externo ou associação de conteúdo
      - modulo: docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
        quando: tratar apresentações ou modos do console multinível
      - modulo: docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md
        quando: houver referência a dado, modo normal ou outro termo legado
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

Pela ADR-0022, a futura tela inicial real `orquestrador` deverá conter um
`console` estruturalmente presente e sem entradas iniciais de dados reais ou
demonstrativos. Isso significa instância declarada no corpo, não criação por
default nem fallback do renderer.

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
| `politica_paginacao` | Define se a instância pagina, o que ocorre quando o conteúdo não cabe e como os chips `[PgUp][PgDn]` são acionados. Ver seção 12. |
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
- `[⇆]` alterna o foco entre consoles quando há pelo menos dois consoles
  focalizáveis na tela (ver §22.1 e §22.2); `[✥]` navega dentro do console
  em foco quando este possui mais de um item navegável (ver §22.4 e §22.8);
- consoles não focados não recebem cursor nem exibem indicador do item corrente.

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

A identidade, a persistência, a reconciliação e o consumo operacional da
seleção múltipla são fechados pela ADR-0034 — ver seção 23.

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
- a ação deve ser **declarativa e resolvida no registro autoritativo da
  implementação** — comando arbitrário é proibido; o `tela.json` não é a
  autoridade de categoria ou compatibilidade;
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
| `permitir_quebra` | Fluxo contínuo. O item começa na próxima linha disponível, usa o espaço restante da página atual — inclusive a última linha disponível — e continua nas páginas seguintes quando necessário. |
| `evitar_quebra` | Sempre começa em página nova. O item começa na primeira linha útil de uma página nova, mesmo quando ainda há espaço na página anterior. Se maior que uma página, continua nas páginas seguintes. O próximo item com a mesma política também espera uma página nova para começar. |
| `permitir_quebra_somente_se_maior_que_pagina` | Mantém junto quando possível. O item pode começar logo após o item anterior: se couber inteiro no espaço restante, permanece na página atual; se não couber no espaço restante mas couber inteiro em uma página vazia, começa inteiro na página seguinte; se for maior que uma página inteira, começa na primeira linha útil da página seguinte e continua nas páginas posteriores. |

`evitar_quebra` e `permitir_quebra_somente_se_maior_que_pagina` não são
equivalentes: `evitar_quebra` nunca aproveita espaço restante da página
anterior — sempre inicia em página nova, mesmo havendo espaço suficiente;
`permitir_quebra_somente_se_maior_que_pagina` aproveita o espaço restante da
página atual sempre que o item cabe inteiro nele, só adiando o início para
a página seguinte quando não cabe no espaço restante.

- chips `[PgUp][PgDn]` **refletem o estado de paginação** — existem quando a
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
| `[⇆]` | Aparece quando a tela possui pelo menos dois consoles focalizáveis (ADR-0031 D14; ver §22.8) |
| `[✥]` | Aparece quando o console focado possui mais de um item navegável; ausente quando não há console focado ou quando o console tem zero ou um item navegável (ADR-0031 D14; ver §22.8) |
| `[␣]` | Existe quando a instância de `console` declara seleção múltipla |
| `[⏎]` | Ativo quando o item em foco tem `acao_enter` válida; inativo caso contrário |
| `[V]` | Existe quando a instância de `console` declara que permite modo verboso |
| `[PgUp][PgDn]` | Existe quando a instância de `console` declara `paginacao: com` |
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
- quando há pelo menos dois consoles focalizáveis, `[⇆]` alterna o foco entre
  esses consoles; `dashboard`, `lancador`, grupos estruturais, consoles não
  navegáveis e consoles navegáveis sem itens navegáveis não entram nessa lista;
- o `console` só é navegável por `[✥]` quando é o console focado e possui mais
  de um item navegável.

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

---

## 19. Fronteira do console como consumidor de conteúdo externo (ADR-0026)

A ADR-0026 (2026-07-17) registra a fronteira normativa do console como
receptor de conteúdo de runtime fornecido por documento externo.

### 19.1 Conteúdo de runtime tem origem externa

O conteúdo de runtime do console tem origem externa: não é codificado
estaticamente no JSON estrutural da tela. O console recebe esse conteúdo
por meio de um documento JSON externo com envelope declarativo.

### 19.2 Conteúdo chega previamente estruturado

O conteúdo multinível chega ao console previamente estruturado para
apresentação, com os níveis hierárquicos declarados explicitamente. O
consumidor lê os níveis como declarados.

### 19.3 Fronteira do consumidor

O consumidor (componente que carrega e usa o documento externo) **não**:

- reconstrói a hierarquia a partir de dados de domínio não normalizados;
- descobre ou infere estrutura semântica que deveria chegar pronta;
- assume responsabilidades geométricas ou de cálculo físico.

As definições de APIs, classes, assinaturas e módulos do consumidor não foram
decididas por esta ADR e permanecem para decisão futura.

### 19.4 Fronteira do renderizador

O renderizador mantém responsabilidade exclusiva sobre toda a representação
física calculada em runtime:

- geometria e dimensões efetivas;
- quebras físicas;
- truncamentos;
- alinhamentos calculados;
- paginação;
- posições finais;
- recuperação após redimensionamento (SIGWINCH).

O documento externo **não** deve conter esses resultados calculados.

### 19.5 Integração com o script produtor

No sistema final, um script será responsável por produzir ou devolver o
documento externo ao fluxo de apresentação. O protocolo concreto de
comunicação com esse script — assinatura, argumentos, transporte, ciclo de
vida — permanece para decisão futura.

### 19.6 Princípio normativo

```text
O JSON externo declara a intenção de apresentação e o conteúdo semântico.
O renderizador calcula a representação física na área disponível.
```

### 19.7 Decisões deferidas

Permanecem para decisão futura, fora do escopo desta seção:

- vínculo entre `tela.json` e o documento externo (nome do campo, mecanismo);
- protocolo de invocação do script produtor;
- suporte ao `tipo: "matriz"` no mesmo mecanismo;
- comportamento diante de fonte ausente ou inválida;
- navegação, seleção, expansão e recolhimento de níveis;
- paginação interativa de conteúdo multinível.

### 19.8 Remissões

- `contrato_json_console.md` — seção 11 (ADR-0026): envelope declarativo do documento externo;
- `contrato_tela_json.md` — seção 31 (ADR-0026): fronteira do JSON estrutural;
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` — terminologia canônica da ADR-0026.

---

## 20. Fluxo de responsabilidade pelo carregamento e entrega do conteúdo externo (ADR-0027)

A ADR-0027 (2026-07-17) formaliza o fluxo de responsabilidade entre ponto de
entrada, loader, modelo e renderizador no carregamento conjunto da tela e do
conteúdo externo.

### 20.1 Ponto de entrada

O ponto de entrada (`demo/demo.py` no ciclo atual da demonstração integrada):

- identifica o cenário;
- carrega o JSON estrutural da tela;
- carrega o JSON externo de conteúdo quando aplicável;
- associa os dois documentos externamente ao JSON estrutural;
- mantém as origens separadas;
- entrega entradas separadas ao fluxo.

O ponto de entrada não é o único artefato de demonstração possível — podem
existir demos dedicados e testes auxiliares —, mas é o único ponto de entrada
obrigatório para provar o comportamento integrado. A responsabilidade pelo
carregamento dos dois documentos pertence ao `demo/demo.py`.

### 20.2 Loader ou camada equivalente

O loader ou camada equivalente:

- lê os documentos;
- valida a estrutura do documento externo segundo os contratos ativos;
- converte o conteúdo externo para representação interna;
- não decide geometria;
- não infere hierarquia.

### 20.3 Modelo

O modelo:

- transporta a estrutura semântica;
- preserva ordem, níveis e relação entre pais e filhos;
- pode compor internamente a tela e seu conteúdo sem apagar a distinção das
  origens;
- não abre arquivos;
- não escolhe a fonte do conteúdo;
- não calcula representação física.

### 20.4 Renderizador

O renderizador:

- recebe a representação semântica;
- produz linhas, colunas, truncamentos, alinhamentos, designadores concretos e
  demais resultados físicos;
- não abre JSONs;
- não escolhe arquivos;
- não reconstrói hierarquia de dados de domínio.

### 20.5 Demonstração real

A demonstração integrada deve ocorrer pelo `demo/demo.py`. Pode usar auxiliares,
mas não pode ser comprovada somente por demo dedicado. A demonstração deve:

- usar JSONs permanentes;
- provar a identidade da tela e do conteúdo;
- ser acessível e reproduzível pelo ponto de entrada real.

Código de saída zero não é prova suficiente da integração.

### 20.6 Fonte futura

No H-0036, a fonte é uma fixture permanente. No produto final, a fonte será
substituída por um script que buscará dados no Pipeline. O console continuará
recebendo o mesmo contrato semântico. O protocolo do script permanece deferido.

### 20.7 Remissões

- `contrato_tela_json.md` — seção 32 (ADR-0027): fronteira do JSON estrutural;
- `contrato_json_console.md` — seção 12 (ADR-0027): schema semântico multinível;
- `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` — terminologia canônica da ADR-0027.

---

## 21. Apresentações de conteúdo multinível, alternância verbosa e estado de sessão (ADR-0028)

A ADR-0028 (2026-07-17) formaliza as regras normativas das apresentações de
conteúdo multinível no `console`, a semântica da tecla `V` e o estado de
visualização da sessão. Esta seção propaga essas regras para o contrato do
`console`.

### 21.1 Escopo exclusivo

Esta seção aplica-se exclusivamente a instâncias de `console` que recebem
conteúdo multinível externo (`tipo: "multinivel"`). O `console` sem conteúdo
externo preserva integralmente o comportamento histórico definido pelos contratos
ativos.

### 21.2 Modo não verboso

No modo não verboso, cada conteúdo aplicável do `console` com dados multinível
ocupa exatamente uma linha física. O excedente é truncado conforme a política
declarada. Os dados originais permanecem inalterados.

### 21.3 Modo verboso

No modo verboso, o conteúdo pode ocupar várias linhas físicas calculadas pelo
renderizador. As linhas de continuação respeitam o alinhamento definido no
documento de conteúdo.

### 21.4 Relação com `modo normal`

O `contrato_console.md` (§6) utiliza o termo **`modo normal`** para o modo
operacional do `console` sem quebra de linha, declarado como default da instância.
A ADR-0028 utiliza o termo **`modo não verboso`** para o mesmo comportamento
conceitual aplicado às apresentações de conteúdo multinível.

Os dois termos descrevem o mesmo comportamento: exibição de cada conteúdo
aplicável em uma única linha física, com truncamento do excedente. A reconciliação
terminológica definitiva é adiada. O registro desta equivalência conceitual não
implica que `modo normal` seja sinônimo de `somente_nao_verboso`: uma tela com
política `alternavel` também pode exibir em modo não verboso sem ser classificada
como somente não verbosa.

### 21.5 Alternância pela tecla V

A disponibilidade da tecla `V` e do chip `[V] Verboso` depende da política de
modo declarada pela tela (D23, §21.11):

- **Telas alternáveis** (`politica_modo: "alternavel"`): a tecla `V` alterna entre
  os estados verboso e não verboso durante a sessão; a barra de menus apresenta
  o chip `[V] Verboso`.
- **Telas de modo único** (`politica_modo: "somente_verboso"` ou
  `"somente_nao_verboso"`): a tecla `V` não é uma ação aplicável; o chip
  `[V] Verboso` não é obrigatório.

A alternância (quando aplicável):

- usa os mesmos dados;
- usa a mesma tela;
- usa o mesmo documento de conteúdo;
- não troca a apresentação;
- não persiste alteração;
- é reversível: uma segunda ativação retorna ao modo anterior.

O `console` sem conteúdo multinível externo não expõe nem utiliza a tecla `V`.

### 21.6 Estado visual da sessão

O estado de visualização verboso/não verboso é um estado da sessão. Ele não
deve:

- reescrever o JSON externo de conteúdo;
- reescrever o JSON estrutural da tela;
- alterar permanentemente uma fixture;
- substituir os dados;
- persistir preferência global;
- vazar para outra instância de `console`;
- alterar a identidade do cenário.

Ao recarregar a tela ou trocar de cenário, o modo inicial volta a ser determinado
pela configuração declarativa carregada.

### 21.7 Modo inicial

O modo inicial é determinado pela política de modo declarada no JSON estrutural da
tela (campo `formato.excesso.politica_modo` do elemento `console`), conforme D23:

- **Tela somente verbosa**: inicia necessariamente em modo verboso;
- **Tela somente não verbosa**: inicia necessariamente em modo não verboso;
- **Tela alternável**: inicia no modo declarado em `formato.excesso.modo_inicial`
  (campo obrigatório para essa política; valores aceitos: `"verboso"`,
  `"nao_verboso"`).

Ao recarregar a tela ou trocar de cenário, o modo inicial volta a ser determinado
pela política declarada carregada.

A definição do modo inicial estava anteriormente adiada conforme ADR-0028 §43
item 3. A revisão D23 encerra esse adiamento para telas novas ou revisadas: a
política ausente é inválida e nenhum default implícito é permitido.

O campo `excesso.modo` que existia no documento JSON externo de conteúdo
(mecanismo anterior ao D23, registrado em `contrato_json_console.md` §12.7) é
supersedido por `formato.excesso.politica_modo` e `formato.excesso.modo_inicial`
no JSON estrutural para telas novas ou revisadas.

### 21.8 Redimensionamento

Após redimensionamento, o modo visual da sessão é preservado. O renderizador
recalcula a representação física com o modo corrente.

### 21.9 Paginação e impossibilidade geométrica

Paginação não resolve impossibilidade horizontal no conteúdo multinível. Quando
nem a unidade mínima couber na área útil, o `console` aciona a política de
impossibilidade geométrica das ADRs vigentes (ADR-0017, ADR-0023).

### 21.10 Remissões

- `contrato_json_console.md` — seção 13 (ADR-0028): regras normativas, validações e política de modo;
- `contrato_barra_de_menus.md` — seção 22 (ADR-0028): chip `[V] Verboso`;
- `contrato_tela_json.md` — seção 33 (ADR-0028): JSON estrutural e política de modo;
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` — terminologia canônica da ADR-0028.

### 21.11 Políticas de modo por tela (D23)

A revisão D23 da ADR-0028 formaliza que cada tela de `console` com conteúdo
multinível nova ou revisada deve declarar uma das três políticas de modo no JSON
estrutural da tela (campo `formato.excesso.politica_modo`).

#### 21.11.1 Tela somente verbosa (`"somente_verboso"`)

- A tela sempre exibe o conteúdo em modo verboso.
- A tecla `V` não é uma ação aplicável.
- O chip `[V] Verboso` não é obrigatório na barra de menus.
- O comportamento visual segue integralmente as regras do modo verboso (§21.3).
- O `console` não precisa declarar `modo_inicial`.

#### 21.11.2 Tela somente não verbosa (`"somente_nao_verboso"`)

- A tela sempre exibe o conteúdo em modo não verboso.
- A tecla `V` não é uma ação aplicável.
- O chip `[V] Verboso` não é obrigatório na barra de menus.
- O comportamento visual segue integralmente as regras do modo não verboso (§21.2).
- O truncamento com `...` permanece válido quando aplicável.
- O `console` não precisa declarar `modo_inicial`.

#### 21.11.3 Tela alternável (`"alternavel"`)

- A tela suporta os dois modos.
- A tecla `V` alterna entre os estados verboso e não verboso.
- O chip `[V] Verboso` é obrigatório na barra de menus.
- O `console` deve declarar `modo_inicial` (`"verboso"` ou `"nao_verboso"`).
- A alternância é reversível: uma segunda ativação retorna ao modo anterior.

#### 21.11.4 Escopo de obrigatoriedade

A obrigação de declarar `politica_modo` aplica-se a telas novas ou revisadas.
Telas legadas (criadas antes da incorporação de D23) permanecem válidas sem
declaração. Ausência de `politica_modo` em tela nova ou revisada é inválida;
nenhum default implícito é permitido.

#### 21.11.5 Cenários futuros mínimos (§36.2)

Quatro cenários mínimos de demonstração estão definidos em `contrato_json_console.md`
§13.13.10, cobrindo as três políticas de modo.

---

## 22. Navegação, foco e seleção única (ADR-0031)

A ADR-0031 (2026-07-25) formaliza as regras operacionais de foco entre consoles
navegáveis de nível único, cursor sobre item lógico, navegação toroidal por eixo,
indicador visual e chips condicionais. Esta seção propaga essas regras para o
contrato do `console`.

### 22.1 Elegibilidade do console

Um `console` é **focalizável** quando satisfaz ambas as condições:

1. Declara navegação habilitada por meio do campo `politica_navegacao` da instância (§3 e §7).
2. Possui ao menos um item com `navegavel: true` (§4).

```yaml
console_focalizavel:
  requisitos:
    - declara_navegacao_habilitada_via_politica_navegacao
    - possui_ao_menos_um_item_com_navegavel_true

console_sem_declaracao_de_navegacao:
  entra_na_lista_de_foco: false
  recebe_cursor: false

console_navegavel_sem_itens_com_navegavel_true:
  entra_na_lista_de_foco: false
  recebe_cursor: false
  exibe_indicador: false

dashboard:
  entra_na_lista_de_foco: false

lancador:
  entra_na_lista_de_foco: false
```

O mecanismo declarativo é `politica_navegacao` (no console) e o campo `navegavel`
(no item). Esta regra não inventa campo ou schema novo — usa os mecanismos
declarativos já presentes em §3, §4 e §7.

### 22.2 Lista de foco e foco entre consoles

A lista de foco da tela contém somente consoles focalizáveis (§22.1). Grupos
estruturais não recebem foco. A lista é produzida por travessia hierárquica em
profundidade da árvore de grupos e elementos do corpo.

```yaml
grupos_estruturais:
  recebem_foco: false

travessia:
  estrategia: PROFUNDIDADE_PRIMEIRO
  resultado: LISTA_LINEAR_ORDENADA

ordem_entre_irmaos:
  horizontal: ESQUERDA_PARA_DIREITA
  vertical: CIMA_PARA_BAIXO
  matriz:
    dentro_da_linha: ESQUERDA_PARA_DIREITA
    entre_linhas: CIMA_PARA_BAIXO
```

Tab percorre a lista no sentido direto (circular). Shift+Tab percorre a mesma
lista no sentido inverso (circular). Ambos são circulares: o último elemento
avança para o primeiro; o primeiro recua para o último.

### 22.3 Entrada em console

Toda entrada em console focalizável — seja na primeira entrada, por Tab, por
Shift+Tab, ou por retorno posterior ao mesmo console pela lista de foco —
posiciona o cursor no item lógico `0`.

```yaml
cursor_destino: ITEM_LOGICO_0
restaurar_cursor_anterior_do_console: false
```

Não existe memória de cursor por console. O retorno ao mesmo console reinicia
sempre no item `0`. Esta regra aplica-se à **entrada** no console; redistribuição
ou mudança de modo do console já focado não reinicia o cursor (ver §22.5).

### 22.4 Navegação interna por item lógico

O cursor navega por item lógico, não por linha física. A ordem lógica dos itens
segue a distribuição declarada:

```yaml
linha: ESQUERDA_PARA_DIREITA
coluna: CIMA_PARA_BAIXO
matriz: ROW_MAJOR
```

As setas navegam somente entre itens ocupados da página e da exibição atuais:

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

**Casos degenerados e matriz incompleta:**

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

Em matriz incompleta, células vazias não participam do toróide e não recebem
cursor. Não há compensação para outra linha ou coluna quando a seta atinge borda
sem item. Setas não mudam de página — cada página é toróide fechado.

### 22.5 Redistribuição e mudança de modo

Enquanto o console permanece focado, redistribuição ou mudança de modo preserva
o item lógico corrente e recalcula os demais atributos visuais:

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

A mudança entre modo verboso e não verboso segue a mesma regra. Redistribuição
ou mudança de modo não reinicia o cursor no item `0`.

### 22.6 Indicador do item corrente

Somente o console com foco exibe o indicador do item corrente. Consoles não
focados não mostram o indicador. Console navegável reserva a coluna do indicador.

```yaml
item_corrente:
  primeira_linha_fisica: INDICADOR_SELECIONADO
  linhas_de_continuacao: ESPACO

demais_itens:
  primeira_linha_fisica: ESPACO
  linhas_de_continuacao: ESPACO
```

O indicador:

- Marca o início lógico do item — aparece somente na primeira linha física do
  item corrente.
- Não é repetido nas linhas de continuação do mesmo item.
- Tem largura reservada estável — a coluna não se desloca ao mudar o cursor de
  item.
- Deve ser obtido do campo `selecionado_simbolo` do objeto de estilo global
  materializado (ADR-0030 D6 e D8). O renderer não recebe autorização para
  hardcodar `→`.

Não se adiciona caractere extra ao título do console para indicar foco. O
indicador visual é exclusivo da coluna `ec` do item corrente dentro do console
focado.

### 22.7 Seleção única

Neste ciclo, seleção única significa o único item sob o cursor:

```yaml
item_corrente:
  quantidade: UM
  identidade: ITEM_SOB_CURSOR
  persistencia_como_conjunto: false
  toggle_por_espaco: false
  indicador_de_inclusao: false
```

`[␣]` e os indicadores de inclusão (`tg` com `●`/`○`) pertencem ao ciclo de
seleção múltipla (ITEM-0006). A execução de ação por `[⏎]` não integra o escopo
desta regra — contratos vigentes podem continuar registrando essa capacidade
futura.

### 22.8 Chips condicionais (ADR-0031 D14)

```yaml
chip_alternancia:
  identificador_canonico: "[⇆]"
  aparece_quando: PELO_MENOS_DOIS_CONSOLES_FOCALIZAVEIS
  nao_aparece_com:
    - zero_consoles_focalizaveis
    - um_console_focalizavel

chip_setas:
  identificador_canonico: "[✥]"
  aparece_quando: CONSOLE_FOCADO_COM_MAIS_DE_UM_ITEM_NAVEGAVEL
  nao_aparece_com:
    - console_sem_itens_navegaveis
    - console_com_um_unico_item_navegavel
    - ausencia_de_console_focado
```

A condição considera consoles **focalizáveis** (§22.1), não apenas consoles
declarados navegáveis sem itens. Não se inventa chip novo neste ciclo.

### 22.9 Fronteiras deste contrato aplicado

Permanecem fora deste contrato aplicado (ADR-0031 D15):

- Paginação interativa por `PageUp` e `PageDown` (ITEM-0003) — a
  especificação foi fechada pela ADR-0038 e especializada universalmente pela
  ADR-0041; ver §24. A implementação permanece pendente e não é antecipada
  por esta seção.
- Catálogo e dispatcher de ações (ITEM-0004 / DOC-B009).
- Abertura e retorno entre telas (ITEM-0005).
- Seleção múltipla (ITEM-0006).
- Navegação multinível e expansão/recolhimento (ITEM-0007).

As regras históricas sobre essas capacidades permanecem quando já existirem
neste contrato — classificadas como futuras ou fora deste ciclo.

### 22.10 Remissões

- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md` — decisões D1–D15;
- `docs/nomenclatura/32_CONSOLE.md` — terminologia canônica;
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` — condições dos chips;
- `docs/contratos/contrato_barra_de_menus.md` — regras da barra e dos chips.

### 22.11 Política declarada e regras transversais da navegação multinível
(ADR-0042, D-MULTI-01, D-MULTI-02, D-MULTI-12, D-MULTI-13)

A navegação multinível é uma política declarada explicitamente na instância do
`console`. `politica_navegacao` permanece um objeto, com `navegavel` mantendo
sua semântica vigente e `tipo` como único discriminador canônico:

```json
"politica_navegacao": {
  "navegavel": true,
  "tipo": "dois_niveis_por_foco"
}
```

Os únicos valores de `tipo` são `nivel_unico`, `tabela`,
`arvore_colapsavel`, `selecao_multinivel` e `dois_niveis_por_foco`. Quando o
campo estiver ausente, o tipo efetivo será `nivel_unico`; a ausência não
invalida a configuração por si só. Não existe segunda forma declarativa e não
se infere `tipo` da estrutura dos dados, da apresentação, do nome da fixture
ou de qualquer outro campo. Não se cria matriz geral de validade entre
`navegavel` e `tipo`.

Tab e Shift+Tab continuam movimentando o foco entre consoles. As setas
movimentam o cursor dentro do console focalizado somente quando a política
permitir. `[✥]` continua sendo indicador de disponibilidade das setas, não
comando. Foco, cursor e seleção permanecem mecanismos distintos; item visível
não navegável não recebe cursor; o nome da fixture não produz comportamento
especial; e políticas com seleção reutilizam a apresentação visual já vigente,
sem nova linguagem visual de seleção.

### 22.12 Política `nivel_unico` (ADR-0042, D-MULTI-03)

`nivel_unico` preserva integralmente o comportamento vigente desta seção: as
quatro setas, a navegação toroidal por eixo, a exclusão de células vazias, a
troca de foco por Tab/Shift+Tab e as demais regras de nível único não são
redesenhadas por ADR-0042.

### 22.13 Política `tabela` (ADR-0042, D-MULTI-04)

`tabela`, quando usada como política de navegação, é passiva: não participa do
foco, não possui cursor entre linhas, não é percorrida pelas setas e não exibe
`[✥]`. Não há fallback para `nivel_unico`. Uma declaração incompatível de
`tabela` como navegável produz falha focal; esta ADR não determina o momento,
a camada ou o mecanismo dessa falha.

### 22.14 Política `arvore_colapsavel` (ADR-0042, D-MULTI-05)

`arvore_colapsavel` é uma árvore hierárquica navegável sem seleção. ↑ e ↓
percorrem a sequência hierárquica atualmente visível. Ao fechar um ramo, seus
descendentes deixam o percurso, mas o próprio ramo permanece item corrente.
Espaço abre ou fecha o ramo. A política não possui seleção, `Todos` ou
semântica nova de Enter.

### 22.15 Política `selecao_multinivel` (ADR-0042, D-MULTI-06, D-MULTI-06-P03, D-MULTI-07-P04)

`selecao_multinivel` admite profundidade arbitrária e reúne todos os níveis em
uma única topologia de navegação. Não há toroide independente por pai, nível
ou ramo. A apresentação pode ocupar múltiplas colunas somente quando a
geometria vigente já permitir; esta política não cria geometria nova.

Todo item selecionável — raiz, pai intermediário ou folha — possui o mesmo
estado binário de seleção, independentemente da profundidade, e usa `tg`. Item
não selecionável não possui estado de seleção, não recebe `tg` e não participa
da unanimidade.

D-MULTI-07-P04 fecha a coerência estrutural da selecionabilidade em
profundidade arbitrária: se um nó possui ao menos um descendente selecionável,
esse nó e todos os seus ancestrais estruturais até a raiz são selecionáveis.
Assim, todo pai com conteúdo selecionável é selecionável, possui estado
binário, apresenta `tg` e participa da política de seleção vigente. Essa
restrição não altera a regra de D-MULTI-06-P03:

```text
pai selecionável marcado ⇔ todos os filhos selecionáveis imediatos marcados
```

O estado do pai continua sendo derivado por unanimidade dos filhos
selecionáveis imediatos, com reconciliação de baixo para cima, sem estado
parcial ou indeterminado. Espaço mantém a propagação descendente vigente sobre
todos os descendentes selecionáveis em qualquer profundidade e, depois, a
reconciliação ascendente dos pais.

Item não selecionável permanece sem estado e sem `tg`, fica fora do conjunto
selecionado e da unanimidade, e não pode possuir descendentes selecionáveis.
Portanto, item não selecionável implica subárvore integralmente não
selecionável; ele pode ser folha ou pai cujo conteúdo inteiro também seja não
selecionável. A configuração abaixo é inválida/incoerente e não pertence ao
domínio válido de `selecao_multinivel`:

```text
pai não selecionável
└── descendente selecionável
```

Não há comportamento funcional de Espaço para essa configuração. Para pais
válidos com conteúdo selecionável, o pai é selecionável, possui `tg` e a
propagação/reconciliação já vigente permanece aplicável.

Para todo pai selecionável, vale a derivação:

```text
selecionado ⇔ todos os filhos selecionáveis imediatos estão selecionados
```

Assim, qualquer filho selecionável imediato desmarcado deixa o pai
desmarcado; filhos não selecionáveis são ignorados; e não existe estado
parcial ou indeterminado. O estado do pai é o mesmo estado binário existente:
não é seleção paralela independente dos filhos, contador, terceiro estado ou
novo símbolo.

Depois de toggle manual de uma folha ou de outro filho selecionável, o pai
imediato e os ancestrais selecionáveis são reconciliados recursivamente de
baixo para cima até a raiz. A mesma cadeia é reconciliada ao desmarcar um
descendente, no sentido ascendente, desmarcando os ancestrais que deixarem de
satisfazer a unanimidade.

Espaço sobre pai mantém a propagação descendente recursiva a todos os
descendentes selecionáveis, em qualquer profundidade: inclui todos ou remove
todos conforme o estado da ação, sem alterar itens não selecionáveis. Depois
dessa propagação, os pais são reconciliados de baixo para cima pela mesma
regra de unanimidade. A apresentação de seleção vigente é reutilizada.

Os critérios demonstrativos aprovados permanecem para etapa posterior: a
fixture futura deve permitir pelo menos três pais de nível 1; dois pais
selecionáveis de nível 2 no primeiro ramo, cada qual com múltiplas folhas
selecionáveis; um caso não selecionável em outro ramo; propagação descendente;
seleção manual ascendente; e desseleção com desmarcação dos ancestrais
afetados. Nenhuma fixture é criada por este contrato.

O caso negativo correto do H-0054 permanece:

```text
2. Pai nível 1 selecionável
   ├── filho selecionável
   └── item não selecionável
```

O pai `2.` possui `tg` e participa da seleção. O item não selecionável não
possui `tg`, não é marcado por propagação, não possui descendentes
selecionáveis e não interfere na unanimidade dos filhos selecionáveis.

### 22.16 Política `dois_niveis_por_foco` (ADR-0042, D-MULTI-07 a D-MULTI-09)

Esta política possui exatamente dois níveis: nível 1 de pais e nível 2 de
filhos diretos de cada pai. Um terceiro nível é inválido. Todos os pais
navegáveis formam um único toroide; cada pai tem seu próprio toroide de
filhos; filhos de pais distintos nunca compartilham toroide; e o toroide de
filhos ativo é determinado pelo pai corrente.

Espaço no nível dos pais entra no toroide de filhos do pai corrente. As setas
operam somente no toroide atualmente ativo. Esc no toroide de filhos retorna
ao toroide dos pais, preserva o filho escolhido, não limpa a escolha e não
possui semântica de cancelamento. Essa precedência é contextual e não altera
as demais políticas.

Cada pai mantém exatamente um filho escolhido: Espaço sobre outro filho
transfere a escolha; Espaço sobre o filho já escolhido mantém a escolha; e
mover o cursor não a transfere. O mecanismo é denominado **seleção exclusiva
obrigatória de filho por pai** e é distinto de `seleção única` da ADR-0031,
que continua designando o item sob cursor.

### 22.17 Paginação das políticas multinível (ADR-0042, D-MULTI-10)

Toda paginação multinível consome integralmente a autoridade da ADR-0041 e a
seção 24 deste contrato: somente `PageUp` e `PageDown`, com `[PgUp][PgDn]`.
Não se cria tecla, chip ou regra concorrente; não há wrap entre páginas; e o
cursor não troca de página implicitamente.

### 22.18 Critério futuro de demonstração (ADR-0042, D-MULTI-11)

Aplicação e handoffs futuros devem demonstrar, para cada política navegável,
console focalizado, cursor visível, item corrente distinguível, movimento
efetivo pelas teclas previstas e `[✥]` quando as setas estiverem disponíveis.
Quando houver mais de um eixo, a geometria existente da fixture deve
demonstrar esses eixos; uma única coluna não demonstra navegação horizontal.
Para `tabela`, a demonstração deve confirmar a ausência de cursor e de
`[✥]`. Esta seção não cria execução, confirmação, cancelamento, persistência,
prévia ou ação posterior à seleção.

---

## 23. Seleção múltipla e fluxo focal de processamento (ADR-0034)

A ADR-0034 (2026-07-28) fecha a identidade, a persistência, a reconciliação e
o consumo operacional da seleção múltipla, referida como `politica_selecao:
multipla` em §8. Esta seção propaga essas decisões para o contrato do
`console`.

### 23.1 Identidade e persistência da seleção (D-SEL-01)

```yaml
selecao_multipla:
  natureza: conjunto_de_ids_estaveis
  escopo: estado_de_runtime_da_sessao
  persistencia_no_json: false
  independencia: por_console
  persiste_entre_paginas: true
  persiste_quando_filtro_apenas_oculta: true
  persiste_entre_sessoes: false
  descartada_ao_sair_ou_recarregar: true
  natureza_de_todos: snapshot_de_ids_no_momento_do_acionamento
```

`Todos` (D-SEL-06) não incorpora automaticamente itens criados após o
acionamento — é um snapshot, não uma consulta dinâmica.

### 23.2 Invariantes de seleção (D-SEL-02)

- todo item selecionável é navegável; item não navegável não pode ser
  selecionável;
- a seleção ativa contém somente IDs existentes, navegáveis e
  selecionáveis no momento da verificação;
- `ec` (cursor) e `tg` (inclusão na seleção) permanecem estados distintos —
  `ec` nunca representa inclusão; `tg` nunca representa posição do cursor;
- posição visual, página, filtro e ordem de marcação não definem identidade
  nem ordem de execução do conjunto selecionado.

### 23.3 Ordem e reconciliação da entrada da operação (D-SEL-03, D-SEL-04)

A entrada da operação consumidora (§23.6) é uma lista sem duplicatas,
ordenada pela ordem lógica estável do `console`.

```yaml
reconciliacao:
  quando: antes_da_execucao_e_apos_atualizacao_dos_dados
  remove:
    - ids_inexistentes
    - itens_que_deixaram_de_ser_selecionaveis
  preserva: ordem_logica_do_console
  executa: somente_ids_validos_restantes

reconciliacao_vazia_apos_enter:
  havia_selecao_antes: true
  torna_se_vazia: true
  efeito:
    executar: false
    aplicar_todos_no_mesmo_acionamento: false
    selecao_resultante: vazia
  proximo_enter_sem_selecao: assume_funcao_todos
```

### 23.4 Teclas `Espaço`, `Enter` e `Esc` (D-SEL-05 a D-SEL-08)

| Tecla | Efeito |
|---|---|
| `Espaço` | Alterna a inclusão do item em foco na seleção; não move o cursor; sem efeito em item não selecionável |
| `Enter` sem seleção | Assume o rótulo `Todos` (§4.5 de `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`); seleciona todos os itens selecionáveis do conjunto filtrado, em todas as páginas; produz snapshot de IDs (§23.1); com zero itens selecionáveis, o chip permanece visível e inativo |
| `Enter` com seleção | Assume o rótulo `Executar`; executa a operação consumidora declarada pelo binding (§23.6); ativação real no Handoff 4 conforme §23.9 e `contrato_barra_de_menus.md` §23.2 |
| `Esc` com seleção ativa | Limpa a seleção; permanece na tela; só volta ao comportamento de navegação depois de limpar |
| `Esc` sem seleção, tela raiz | Sai |
| `Esc` sem seleção, demais telas | Volta |

### 23.5 Indicadores e chip `Espaço` (D-SEL-09, D-SEL-10)

- `ec` aparece somente no item sob cursor;
- `tg` existe somente em item selecionável e mostra o símbolo do estilo global
  para incluído (`●`) ou não incluído (`○`); item não selecionável não possui
  estado de seleção nem recebe `tg`;
- o chip `Espaço` existe quando a instância declara `politica_selecao:
  multipla`; fica ativo quando o item atual é selecionável e inativo quando
  não é.

O universo de `Todos` é composto pelos itens selecionáveis do conjunto
filtrado, incluindo todas as páginas. Alterar o filtro altera visibilidade,
mas não remove IDs já selecionados nem limita posteriormente a execução de
uma seleção já formada. A prova de persistência entre páginas e a paginação
interativa do console permanecem no `ITEM-0003`.

### 23.6 Operação consumidora e fronteira com ações genéricas (D-SEL-11; ADR-0035)

A operação sobre o conjunto selecionado pertence ao binding ou à origem de
dados consumida pelo `console` — nunca ao renderer, à instância genérica do
`console` como regra global, nem à tela inteira.

```yaml
entrada_da_operacao:
  tipo: lista_ordenada_de_ids_reconciliados
  ids_duplicados: proibidos
  lista_vazia: proibida
  objetos_completos: nao_transportados
```

A ADR-0035 especializa a fronteira comportamental do Handoff 2 sobre essa
entrada, sem substituir a ADR-0034 nem alterar D-SEL-01 a D-SEL-10:

```yaml
handoff_2_fronteira_comportamental:
  recebe: lista_ordenada_de_ids_reconciliados
  consulta_sintetica_para_produzir_itens: ausente
  transporte_de_objetos_completos: proibido
  executor: sintetico_demonstrativo
  fixture: sintetica_demonstrativa
  binding_real: ausente
  operacao_do_pipeline: ausente
  dry_run:
    altera_dados: false
  execucao_real:
    altera: somente_copia_temporaria_da_fixture
  item_ja_processado: ignorado
  id_textual_inexistente: nao_encontrado
  ordem_dos_resultados: preserva_ordem_dos_ids_recebidos
```

Permanecem fora deste contrato aplicado e fora do Handoff 2: registry
genérico de ações, dispatcher genérico, catálogo genérico de ações,
comandos arbitrários declarados no JSON e ativação da interface
(`Enter`/`Executar`) — responsabilidades do `ITEM-0004` ou do Handoff 4.
Schema completo do documento de resultado, CLI provisória, diretório
temporário e controles sintéticos pertencem a `contrato_json_console.md`
seção 14.

A ADR-0036 (2026-07-29) especializa, para a tela padrão de resultado, a
fronteira comportamental do Handoff 3 sobre essa mesma entrada, sem
substituir a ADR-0034 nem a ADR-0035:

```yaml
handoff_3_fronteira_comportamental:
  carrega: tela_json_e_documento_runtime_uma_vez_cada
  valida_antes_da_construcao: true
  constroi_modelo_composto_em_memoria: true
  redesenho_ou_SIGWINCH: nao_rele_arquivos
  escolhe:
    documento_de_resultado_quando: codigo_saida_0_e_documento_valido
    envelope_de_erro_quando:
      - codigo_saida_nao_zero
      - resultado_ausente
      - resultado_malformado
      - resultado_semanticamente_invalido
  abre_tela_de_resultado: false
  executa_retorno: false
```

A abertura da tela de resultado e a execução do retorno pertencem
exclusivamente ao Handoff 4 (ADR-0036 D-H3-19) — ver §23.7.

### 23.6.1 Transmissão do modo universal junto ao lote reconciliado (ADR-0040)

Em operação baseada em seleção, a tela captura o modo corrente no instante do
acionamento e transmite explicitamente `executar` ou `dry_run` na requisição;
o modo capturado acompanha explicitamente o lote reconciliado quando aplicável.
O modo não integra a identidade
do lote, não altera a seleção nem a reconciliação e não é propriedade do
console.

O executor recebe o modo pela requisição já construída e não consulta
diretamente o estado da interface. Alteração posterior do chip não modifica
uma requisição iniciada. Foco, cursor, seleção e página continuam mecanismos
independentes; a regra universal é da instância da tela, não do console.

Antes dessa transmissão, a ação relevante deve ser resolvida no registro
autoritativo da implementação. A categoria e os modos aceitos não podem ser
declarados, contraditos ou falsificados pelo JSON ou pelo console. Ausência do
registro, categoria ausente ou desconhecida e processo sem declaração suficiente
falham de forma fechada antes da execução; navegação e visualização não
participam da exigência de aceitar os dois modos. O console pode referenciar ou
acionar a ação, mas não é proprietário de sua categoria ou compatibilidade.

### 23.7 Fronteiras deste contrato aplicado (ADR-0034 D-SEL-26; supersessões ADR-0036 D-H3-19 e ADR-0037 D-H4-04)

Permanecem fora deste contrato aplicado: registry e dispatcher genéricos de
ações (`ITEM-0004`); pilha genérica de telas (`ITEM-0005`); paginação
interativa (`ITEM-0003` — especificação fechada pela ADR-0038, ver §24;
implementação pendente); seleção compartilhada entre consoles compatíveis;
implementação do controle universal e futura reconciliação da instância focal
(`ITEM-0020`); colapso e expansão multinível (`ITEM-0007`).

A ADR-0036 substitui pontualmente, quanto à tela de resultado, a divisão
original de D-SEL-21: a ativação do chip `Executar`, a abertura da tela de
resultado, a suspensão da tela de origem, o retorno e a restauração
pertencem exclusivamente ao Handoff 4. O Handoff 3 permanece limitado ao
carregamento, à validação, à construção do modelo, à escolha entre
documento e envelope de erro, e à materialização/apresentação do conteúdo
(§23.6).

A ADR-0037 substitui pontualmente: a proibição de chip de `dry-run` em
D-SEL-19 da ADR-0034; a fronteira correspondente do `contrato_barra_de_menus.md`;
os fora de escopo da ADR-0036 sobre escolha de `dry-run` pela interface e
sobre definição concreta de `cor_alerta`. Todas as demais decisões das
ADRs 0034, 0035 e 0036 permanecem vigentes. A especialização completa do
Handoff 4 está em §23.9.

### 23.8 Remissões

- `docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md` — decisões D-SEL-01 a D-SEL-26;
- `docs/adr/ADR-0035-protocolo-focal-execucao-sintetica-reversivel.md` — especialização do Handoff 2 (H2-ESP-01 a H2-ESP-18);
- `docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md` — especialização do Handoff 3 e supersessão parcial da divisão H3/H4 (D-H3-19);
- `docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md` — especialização do Handoff 4 (D-H4-01 a D-H4-10);
- `docs/contratos/contrato_json_console.md` — seção 14: protocolo provisório, resultado estruturado e envelope de erro;
- `docs/contratos/contrato_barra_de_menus.md` — seção 23: rótulos dinâmicos `Todos`/`Executar`, chip `Espaço` e `[Ins] Dry-Run`;
- `docs/contratos/contrato_tela_json.md` — seção 34: perfil `resultado_execucao`;
- `docs/contratos/contrato_composicao_corpo.md` — tela de resultado como composição;
- `docs/nomenclatura/32_CONSOLE.md` — terminologia de seleção múltipla e reconciliação.
- `docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md` — controle universal e transmissão explícita do modo.

### 23.9 Handoff 4 — integração focal, origem suspensa e retornos (ADR-0037)

A ADR-0037 especializa o Handoff 4 do `ITEM-0006`. Preserva as fronteiras dos
H-0041, H-0042 e H-0043 — não reimplementa protocolo nem construção de
resultado.

#### Transição atômica (D-H4-06)

```text
reconciliar seleção
→ capturar modo
→ preservar referência da origem
→ executar protocolo do H-0042
→ classificar resultado
→ construir modelo do H-0043
→ suspender origem
→ ativar resultado_execucao
```

Proibido:

- tela de resultado vazia;
- estado intermediário de carregamento;
- reimplementação do H-0042 ou H-0043;
- mutação da origem enquanto o resultado estiver aberto;
- pilha genérica de telas.

#### Origem suspensa (D-H4-07)

```yaml
cardinalidade: zero_ou_uma
representacao: referencia_para_instancia_viva
snapshot: proibido
reconstrucao: proibida
```

Preservar na origem suspensa: dados carregados; filtro; página; foco;
cursores; seleção; estado de `dry-run`. Enquanto `resultado_execucao`
estiver ativa, a origem não recebe entrada nem sofre mutação.

#### Retorno após `dry-run` (D-H4-08)

- não recarregar binding;
- preservar seleção, filtro, página, foco e cursor;
- manter `dry_run_ativo: true`;
- recalcular apenas a geometria em caso de redimensionamento.

#### Retorno após execução real (D-H4-09)

Aplicável a sucesso, parcial, falha operacional, resultado inválido e
interrupção `130`:

- limpar seleção;
- recarregar binding;
- reaplicar filtro;
- preservar foco quando válido;
- fallback para primeiro console focalizável;
- preservar cursor pelo ID quando válido;
- fallback para primeiro item navegável;
- retornar com `dry_run_ativo: false`.

#### Limpeza por propriedade (D-H4-10)

- H-0042 limpa temporários e subprocesso;
- H-0043 mantém apenas o modelo em memória;
- H4 limpa suas referências e estado de transição;
- exceção interna do H4 não vira envelope operacional;
- terminal e referências próprias são restaurados por `finally`;
- erro interno é propagado.

---

## 24. Paginação interativa limitada (ADR-0038; tecla e notação especializadas pela ADR-0041)

A ADR-0038 (2026-07-29) fecha a paginação interativa do `console`, deferida
pela ADR-0031 (D15) para o `ITEM-0003`. Esta seção propaga as 14 decisões
fechadas (D-PAG-01 a D-PAG-14) para o contrato do `console`, especializando
a paginação já prevista em §12 e as seções 22 (navegação e foco, ADR-0031) e
23 (seleção múltipla e fluxo focal, ADR-0034/0035/0036/0037) quanto à
interação com página.

A ADR-0041 (2026-08-07) especializa pontualmente D-PAG-14 desta seção
(§24.11): a tecla de acionamento passa a ser exclusivamente `PageUp`/
`PageDown` e a representação visual passa a ser `[PgUp][PgDn] Páginas`,
substituindo `,`/`<`/`.`/`>` e a notação `[<][>]` em todos os documentos
normativos. Nenhuma outra decisão D-PAG-01 a D-PAG-13 é reaberta ou alterada
por esta especialização.

### 24.1 Topologia limitada entre páginas (D-PAG-01)

```yaml
topologia: LIMITADA
primeira_pagina:
  pagina_anterior: INATIVA
ultima_pagina:
  proxima_pagina: INATIVA
wrap_entre_paginas: false
```

Não há transição circular entre a primeira e a última página. Esta topologia
é distinta da navegação toroidal por eixo já fixada pela ADR-0031 (D8, D9;
§22.4) para o movimento do cursor **dentro** de uma mesma página: dentro da
página, o cursor faz wrap toroidal por linha e por coluna; entre páginas, não
há wrap.

### 24.2 Troca explícita de página (D-PAG-02)

```yaml
evento: TROCA_EXPLICITA_DE_PAGINA
preservar_console_focado: true
cursor_destino: PRIMEIRO_ITEM_NAVEGAVEL_DA_PAGINA_DE_DESTINO
preservar_posicao_fisica: false
preservar_ordinal_da_pagina_anterior: false
```

A troca de página é transição de runtime dentro do mesmo console focado — não
é nova entrada por foco (distinta, portanto, da entrada tratada em §22.3). O
cursor não preserva posição física nem ordinal da página anterior; é
reposicionado no primeiro item navegável da página de destino.

### 24.3 Página sem item navegável (D-PAG-03)

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

Uma página pode conter conteúdo visível e nenhum item navegável. A página
permanece acessível e normalmente exibida; o console permanece focado; as
setas não produzem movimento; os controles `[PgUp][PgDn]` continuam
operáveis conforme sua própria condição; não há salto automático de página
nem reorganização de conteúdo para introduzir item navegável artificial.

### 24.4 Universo do chip `[✥]` restrito à página atual (D-PAG-04)

```yaml
universo_de_avaliacao: PAGINA_ATUAL
presente_quando: MAIS_DE_UM_ITEM_NAVEGAVEL_NA_PAGINA_ATUAL
ausente_quando:
  - ZERO_ITENS_NAVEGAVEIS_NA_PAGINA_ATUAL
  - UM_ITEM_NAVEGAVEL_NA_PAGINA_ATUAL
itens_em_outras_paginas_influenciam: false
```

Esta decisão especializa, para console paginado, a condição de existência de
`[✥]` fixada pela ADR-0031 D14 (§22.8): o universo relevante passa a ser a
página atual do console focado, não o total de itens navegáveis do console
em todas as páginas. Itens navegáveis presentes apenas em outras páginas não
fazem `[✥]` aparecer nem permanecer.

### 24.5 Retorno ao console por foco em console paginado (D-PAG-05)

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

Esta decisão especializa, para console paginado, a regra de entrada sempre no
item lógico `0` (ADR-0031 D6; §22.3): cada console mantém seu estado de
página durante a sessão; ao retornar por Tab ou Shift+Tab, a página anterior
do console é preservada, mas o cursor não é restaurado ao item anterior — é
reposicionado no primeiro item navegável da página preservada. Se essa página
não tiver item navegável (§24.3), o cursor permanece sem exibição visível.

### 24.6 Repaginação por redimensionamento e mudança de modo (D-PAG-06)

```yaml
eventos:
  - REDIMENSIONAMENTO
  - MUDANCA_DE_MODO
preservar: ITEM_LOGICO_CORRENTE
pagina_apos_recalculo: PAGINA_QUE_PASSA_A_CONTER_O_ITEM_CORRENTE
preservar_numero_anterior_da_pagina: false
```

Estende às páginas o mesmo princípio já fixado por ADR-0031 D10 (§22.5) para
redistribuição e mudança de modo dentro de uma página: o item lógico corrente
é preservado; a página que passa a contê-lo após o recálculo pode ter número
diferente do anterior, sem que esse número anterior seja preservado como
referência.

### 24.7 Filtros e paginação (D-PAG-07 a D-PAG-09)

Filtros continuam sendo aplicados antes da paginação (§11, §12, R-4).

```yaml
filtro_oculta_item_corrente:
  destino_do_cursor:
    prioridade_1: PROXIMO_ITEM_NAVEGAVEL_NA_ORDEM_LOGICA_DO_CONJUNTO_FILTRADO
    prioridade_2: ITEM_NAVEGAVEL_ANTERIOR_SE_NAO_HOUVER_PROXIMO
  pagina_resultante: PAGINA_QUE_CONTEM_O_NOVO_ITEM_CORRENTE
  preservar_referencia_ao_item_oculto: false

filtro_zera_itens_navegaveis:
  pagina_exibida: PRIMEIRA_PAGINA_DO_RESULTADO_FILTRADO
  console_permanece_focado: true
  cursor_visivel: false
  item_corrente: nenhum
  setas: SEM_MOVIMENTO

remocao_de_filtro:
  restaurar_item_anterior_ao_filtro: false
  preservar: ITEM_LOGICO_CORRENTE_APOS_RECONCILIACAO
  pagina_resultante: PAGINA_QUE_CONTEM_O_ITEM_CORRENTE_ATUAL
  memoria_especial_de_cursor_por_filtro: ausente
```

O resultado filtrado ainda pode possuir conteúdo visível não navegável.
Remover o filtro não desfaz a reconciliação já realizada — não há memória
especial de cursor por filtro para restaurar o item corrente anterior ao
filtro.

### 24.8 Atualização genérica dos dados e precedência da ADR-0037 (D-PAG-10)

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

Esta é a regra genérica de atualização dos dados para o `ITEM-0003`. Ela não
substitui a reconciliação especializada por ID já fixada pela ADR-0037 para o
retorno após execução real do Handoff 4 do `ITEM-0006` (D-H4-09; §23.9): no
fluxo especializado da ADR-0037, o cursor é preservado pelo ID do item
anterior quando este continuar válido, com fallback no primeiro item
navegável — não no "próximo item navegável com base na posição lógica
anterior" desta seção. As duas regras operam em fronteiras distintas e
coexistem sem contradição: esta seção 24.8 é a regra padrão do `ITEM-0003`
para atualizações genéricas fora do fluxo focal de execução real da
ADR-0037; onde os dois conjuntos poderiam se sobrepor, prevalece a regra
especializada de §23.9.

### 24.9 Indicador de página (D-PAG-11, D-PAG-12)

```yaml
uma_pagina:
  indicador: "página 1/1"
  pagina_anterior: INATIVA
  proxima_pagina: INATIVA

conjunto_vazio:
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

Quando a paginação estiver habilitada na instância de `console`, o indicador
é sempre visível — inclusive com uma única página e com conjunto vazio de
itens visíveis. Não existe estado visual `página 0/0`.

### 24.10 Independência de página por console (D-PAG-13)

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

O estado de página é independente por console — mesmo princípio de
independência já fixado para foco (ADR-0031) e para seleção múltipla
(ADR-0034 D-SEL-01; §23.1). Os comandos de página (§24.11) são dirigidos
exclusivamente ao console focado, sem alterar o estado de página de nenhum
outro console nem o foco corrente.

### 24.11 Entradas aceitas (D-PAG-14, especializada por ADR-0041 D-PGU-01 a D-PGU-04)

```yaml
pagina_anterior:
  entradas_aceitas: ["PageUp"]
proxima_pagina:
  entradas_aceitas: ["PageDown"]
chips_exibidos:
  anterior: "[PgUp]"
  proxima: "[PgDn]"
representacao_canonica: "[PgUp][PgDn] Páginas"
caracteres_sem_funcao_de_paginacao: ["<", ">", ",", "."]
```

Esta decisão não define leitura por scan code, keycode físico nem dependência
de layout de teclado — a fronteira de captura e tradução de tecla física para
`PageUp`/`PageDown` permanece de implementação. Os caracteres `<`, `>`, `,`
e `.` deixam de possuir qualquer função de paginação — não são alias,
atalho nem fallback de `PageUp`/`PageDown` (ADR-0041 D-PGU-04).

### 24.12 Relação com seleção múltipla e persistência entre páginas

A independência de página (§24.10) e a repaginação (§24.6 a §24.8) não
alteram a identidade da seleção múltipla como conjunto de IDs estáveis nem
sua persistência entre páginas, já fixadas pela ADR-0034 (D-SEL-01, D-SEL-02,
D-SEL-10; §23.1, §23.2). Posição visual e página não definem identidade nem
ordem de execução do conjunto selecionado — esta seção opera exclusivamente
sobre cursor e página, nunca sobre a seleção.

### 24.13 Remissões

- `docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md` — decisões D-PAG-01 a D-PAG-14;
- `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md` — decisões D-PGU-01 a D-PGU-08, especialização de tecla e representação visual de `[<][>]`;
- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md` — D6, D8, D9, D10, D14, D15, especializados por esta seção;
- `docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md` — D-SEL-01, D-SEL-02, D-SEL-10, preservados sem alteração;
- `docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md` — D-H4-09, cuja precedência sobre §24.8 é explícita;
- `docs/contratos/contrato_barra_de_menus.md` — seção 24: paginação limitada e independência por console;
- `docs/contratos/contrato_chip.md` — regras de existência e ativo/inativo de `[PgUp][PgDn]`, entradas aceitas;
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` — terminologia de paginação limitada e repaginação;
- `docs/nomenclatura/32_CONSOLE.md` — terminologia de página como estado independente por console.

---

## 25. Formatação dos filhos de `dois_niveis_por_foco` (ADR-0047)

A ADR-0047 (2026-08-15) fecha a evolução exclusiva de apresentação/formatação
dos filhos da política `dois_niveis_por_foco` (§22.16; ADR-0042), sem
redesenhar navegação, seleção ou o schema semântico já fechados. O schema
literal declarativo está em `contrato_tela_json.md` §36. Esta seção propaga
o comportamento correspondente.

### 25.1 Escopo

Esta seção aplica-se exclusivamente à formatação física dos filhos quando
`politica_navegacao.tipo = "dois_niveis_por_foco"`. Ela não redefine
`dois_niveis_por_foco` como política de navegação (§22.16), não altera a
seleção exclusiva obrigatória de filho por pai, não cria terceiro nível e
não transforma o console em passivo.

### 25.2 Ordem física do filho e tabulação

A ordem física do filho é:

```text
tabulacao → ec → tg, quando existir → designador, quando existir → conteúdo
```

A tabulação começa antes de `ec`, como recuo aplicado antes do início da
estrutura `ec`/`tg`/`tx` já fixada por `docs/nomenclatura/32_CONSOLE.md`
§4.4. Cursor do filho, toggle do filho, designador do filho e conteúdo do
filho são deslocados para a direita como uma unidade inteira — nunca
apenas o texto. O cursor do filho fica sempre para dentro do primeiro
caractere visual do item pai. É proibido recuar somente o texto deixando
`ec` ou `tg` alinhados ao pai: os dois espaços continuam coexistindo em
posições distintas e adjacentes, sem sobreposição.

Os limites de tabulação são declarados em
`formato.dois_niveis_por_foco.filho.tabulacao` (`contrato_tela_json.md`
§36.3), nunca no documento externo de conteúdo. O renderer usa o maior
valor de tabulação que couber dentro do intervalo declarado: o mínimo se
somente o mínimo couber, um valor intermediário se este couber, ou o
máximo se o máximo couber. Sobra após o máximo permanece à direita da
apresentação, sem ampliação artificial de tabulação. Os valores concretos
pertencem à configuração de cada tela — para as telas desta atividade,
mínimo 5 e máximo 10 — e não são hardcoded no renderer.

### 25.3 Designador

O designador do nível filho usa exclusivamente os mecanismos já existentes
no schema semântico multinível (`contrato_json_console.md` §12.3). Nenhuma
identidade lógica nova é criada, e a ausência de designador é estritamente
visual.

Para tipos visuais (`decimal_composto`, `alfabetico_maiusculo`), o
renderer emite:

```text
designador_visual = prefixo + designador_base + sufixo
```

Ausência de `prefixo` ou `sufixo` equivale a string vazia. Para
`tipo: nenhum`, nenhum designador é emitido.

### 25.4 Apresentação tabular local

`apresentacao = "tabela"` (`contrato_tela_json.md` §36.5) é exclusivamente
forma de apresentação dos filhos. Ela não altera `politica_navegacao.tipo`,
não transforma a política em `tabela` (§22.13), não torna o console
passivo e não cria terceiro nível. Cada filho continua sendo um único item
lógico — cada linha física da apresentação tabular pertence ao mesmo item
lógico filho (distinção item lógico × linha física já fixada por §22.4 e
`docs/nomenclatura/32_CONSOLE.md` §4.4).

A apresentação tabular local não possui cabeçalho, linha separadora, borda
própria nem título próprio.

### 25.5 Colunas

A largura natural de cada coluna deriva do conteúdo real. O cálculo
considera todos os filhos do console, inclusive filhos de pais diferentes:
não existe grade independente por pai. Trocar o pai em foco não faz as
colunas mudarem horizontalmente. O JSON não armazena largura física final,
posição final, quebra física pronta nem geometria calculada de colunas
(§19.4) — esses resultados pertencem exclusivamente ao renderer.

### 25.6 Espaçamento entre colunas

Os limites de espaçamento entre colunas são declarados em
`formato.dois_niveis_por_foco.filho.tabela.espacamento`
(`contrato_tela_json.md` §36.5). O renderer usa o maior valor que couber
entre mínimo e máximo. Se o máximo couber e ainda houver largura
disponível, a sobra fica à direita de toda a tabela — as colunas não são
artificialmente ampliadas para consumi-la. Os valores concretos pertencem
à configuração de cada tela — para a configuração desta atividade, mínimo
3 e máximo 8.

### 25.7 Quebra de conteúdo

Quando a apresentação não couber mesmo após reduzir tabulação e
espaçamento até seus mínimos, células quebram em múltiplas linhas. O item
lógico permanece único: a linha de continuação não cria cursor, não cria
toggle e não cria identidade lógica — o mesmo princípio já aplicado a
linhas de continuação em modo verboso (§21.3, §22.6; módulo `44` §8B).

Resize recalcula a geometria — tabulação efetiva, larguras de coluna,
espaçamento entre colunas e quebras — preservando o item lógico, na mesma
linha já fixada para o console em geral (ADR-0031 D10; §21.8, §22.5). Nenhuma
nova exceção a essa regra é criada para `dois_niveis_por_foco`.

### 25.8 Remissões

- `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md` — decisões
  D-DNF-01 a D-DNF-11 e schema literal fechado em §4.13;
- `contrato_tela_json.md` — seção 36: schema literal declarativo;
- `contrato_json_console.md` — seção 15: fronteira com o documento externo
  de conteúdo;
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` —
  terminologia canônica da ADR-0047;
- `docs/nomenclatura/32_CONSOLE.md` — unidade inteira do filho deslocada,
  `ec`, `tg`, item lógico.
\n