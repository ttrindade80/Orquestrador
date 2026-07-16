---
name: ADR-0013-ocupacao-vertical-janela-terminal-corpo
description: Ocupacao vertical da janela do terminal pelo corpo passa a ser dimensao explicita do render; preenchimento de linhas em branco e responsabilidade do renderer; nao confundir com corpo.arranjo; nao implementa codigo nem testes
metadata:
  type: adr
  status: aceita
  data: 2026-07-09
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/NOMENCLATURA.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
  handoffs_bloqueados: []
---

# ADR-0013 — Ocupação vertical da janela do terminal pelo corpo

## Status

`aceita`

## Data

2026-07-09

## Contexto

Após a ADR-0011 (terminologia de arranjo `vertical`/`horizontal`) e a ADR-0012
(`barra_de_menus` declarativa por tela), o levantamento técnico/documental em
modo somente leitura constatou o seguinte estado corrente da renderização:

- `tela/demo.py` lê apenas a **largura** do terminal por
  `shutil.get_terminal_size(...).columns`;
- `tela/renderizador.py` recebe apenas **largura**, não altura — `renderizar_tela`
  assina `largura` e deriva `inner_w`/`content_w`/`label_max` a partir dela;
- o corpo ocupa a largura disponível, mas **não preenche a altura disponível**
  da janela do terminal — não existe `altura_disponivel`, `rows` nem
  preenchimento vertical do corpo;
- o conceito de "vertical" já está normatizado para `corpo.arranjo`, mas como
  **ordem/composição dos elementos do corpo** (ADR-0011), não como ocupação da
  altura do terminal.

Esses dois significados de "vertical" coexistem e não devem ser confundidos:
`corpo.arranjo = "vertical"` é arranjo de composição; ocupar a altura da janela
do terminal é outra coisa. Sem uma ADR específica para a ocupação vertical da
janela, uma ADR futura sobre `arranjo vertical/horizontal` poderia ser lida de
forma ambígua e sobrescrever/acumular indevidamente essa decisão.

A decisão gerencial é normatizar a **ocupação vertical da janela do terminal
pelo corpo** como decisão arquitetural autônoma, com termo específico próprio,
distinto de `corpo.arranjo`.

Esta ADR é normativa. Ela **não** implementa altura dinâmica no renderer, **não**
altera `tela/`, **não** altera testes e **não** altera JSONs de produção — essas
são pendências de handoff futuro.

---

## Decisão

As declarações abaixo constituem a decisão formal desta ADR.

**1. A tela textual deve ocupar a largura e a altura disponíveis da janela do
terminal.**

A renderização da tela passa a tratar a janela do terminal como uma área
bidimensional: largura já tratada dinamicamente; altura deve passar a ser
tratada como dimensão explícita do render.

**2. A largura já é tratada dinamicamente; a altura deve passar a ser tratada
como dimensão explícita do render.**

Hoje apenas a largura é propagada (`demo.py` lê `.columns`; `renderizar_tela`
recebe `largura`). Esta ADR fixa que a altura deve ser incorporada ao
pipeline de renderização como dimensão de primeiro nível, com termo específico
próprio — não como subproduto de `corpo.arranjo`.

**3. O corpo deve ocupar a altura disponível entre cabeçalho e barra_de_menus.**

A região do corpo ocupa a altura da janela entre o `cabecalho` (acima) e a
`barra_de_menus` (abaixo). A ocupação é da **região do corpo**, não do
`cabecalho` nem da `barra_de_menus`.

**4. Quando o conteúdo funcional do corpo não ocupar toda a altura disponível,
o renderer deve preencher o espaço restante com linhas em branco.**

O preenchimento vertical é comportamento do renderer quando o conteúdo
declarado não preenche toda a altura disponível. Esse preenchimento não é
novo conteúdo, não é novo elemento do corpo e não é novo arranjo — é
preenchimento visual da área do corpo.

**5. O preenchimento vertical do corpo é responsabilidade do renderer, não do
JSON.**

A declaração de ocupação vertical não pertence à instância concreta do
`tela.json`. O renderer recebe (ou calcula) a altura disponível e decide o
preenchimento. O JSON não declara linhas de preenchimento.

**6. A decisão não altera a semântica de `corpo.arranjo`.**

`corpo.arranjo` permanece exatamente como definido pela ADR-0011:
ordem/composição dos elementos funcionais do corpo. Esta ADR não introduz
novo valor de arranjo, não altera `vertical`/`horizontal` e não cria alias.

**7. `corpo.arranjo = "vertical"` significa ordem/composição vertical dos
elementos, não ocupação da altura do terminal.**

`corpo.arranjo = "vertical"` (ADR-0011) dispõe elementos um sobre o outro; é
composição. Ocupar a altura da janela do terminal é outro conceito. Os dois
podem coexistir em uma mesma tela, mas são independentes: uma tela com
`corpo.arranjo = "horizontal"` também deve poder ocupar a altura disponível,
e uma tela com `corpo.arranjo = "vertical"` também deve poder ocupá-la.

**8. A ocupação vertical da janela deve usar termo específico, por exemplo:**

- `ocupacao_vertical_terminal`;
- `preenchimento_altura_corpo`;
- `altura_disponivel`.

A lista acima é de termos específicos completos para esta decisão. Handoffs,
contratos e implementações devem usar um deles (ou equivalente igualmente
específico), nunca a substring ambígua `vertical` sozinha.

**9. O handoff futuro que implementar essa ADR deve decidir a representação
exata das linhas de preenchimento:**

- linhas visuais vazias dentro da caixa do corpo; ou
- linhas físicas vazias com largura total;

mas não pode confundir essa decisão com arranjo de composição.

A representação das linhas em branco é decisão de implementação do handoff
futuro. O que esta ADR fixa é a obrigação de ocupar a altura disponível; a
forma exata (linha visual interna vs. linha física total) fica adiada para o
handoff, desde que não seja tratada como novo arranjo nem novo tipo de
elemento do corpo.

**10. Esta ADR não implementa código nem altera testes agora.**

Esta ADR não altera `config/`, `tela/`, nem artefatos de teste. A
propagação da altura do terminal, o cálculo de `altura_disponivel` e o
preenchimento vertical do corpo são pendências de handoff futuro. Esta ADR
apenas fixa a norma.

### Disambiguação obrigatória de termos

A ocupação vertical da janela **não colapsa** com os campos abaixo, que
continuam independentes:

| Termo específico | Significado | Status |
|---|---|---|
| `corpo.arranjo = "vertical"` | Ordem/composição vertical dos elementos do corpo (ADR-0011) | terminologia final |
| `corpo.arranjo = "horizontal"` | Ordem/composição horizontal dos elementos do corpo (ADR-0011) | terminologia final |
| `ocupacao_vertical_terminal` | Preenchimento da altura da janela do terminal pela tela (esta ADR) | termo específico novo |
| `preenchimento_altura_corpo` | Linhas em branco adicionadas pelo renderer para ocupar a altura do corpo | termo específico novo |
| `altura_disponivel` | Altura entre `cabecalho` e `barra_de_menus` que o corpo pode ocupar | termo específico novo |

`corpo.arranjo = "vertical"` **não é** sinônimo de `ocupacao_vertical_terminal`.
Uma tela com `corpo.arranjo = "horizontal"` também deve ocupar a altura
disponível. A substring `vertical` sozinha é ambígua e não deve ser usada
como critério de alteração normativa (ver ADR-0014, Parte B).

---

## Consequências

### Obrigatórias

- **Renderer futuro deverá receber ou calcular altura disponível.** O
  `renderizar_tela` futuro deve admitir uma dimensão vertical (e.g.
  `altura_disponivel` ou equivalente), derivada ou propagada a partir da
  janela do terminal.
- **Demo futuro deverá propagar altura do terminal, não apenas largura.** O
  `demo.py` futuro deve ler também `.lines` de `shutil.get_terminal_size` (ou
  equivalente) e repassá-la ao renderer.
- **Testes futuros deverão validar ocupação vertical.** Casos de teste
  futuros devem verificar que o corpo preenche a altura disponível entre
  `cabecalho` e `barra_de_menus`, inclusive com preenchimento de linhas em
  branco quando o conteúdo declarado for menor.
- **Contratos devem distinguir `corpo.arranjo = "vertical"` de
  `ocupacao_vertical_terminal`.** `contrato_tela_json.md`,
  `contrato_composicao_corpo.md` e `NOMENCLATURA.md` devem registrar a
  distinção entre composição vertical e ocupação vertical da janela.
- **Handoffs futuros devem usar termos específicos completos.** Handoff de
  implementação da ocupação vertical deve nomear o campo/conceito afetado
  (`ocupacao_vertical_terminal`, `preenchimento_altura_corpo`,
  `altura_disponivel`) e nunca a substring `vertical` sozinha.

### Artefatos a atualizar nesta tarefa documental

| Arquivo | Atualização mínima |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0013 |
| `docs/NOMENCLATURA.md` | Registrar que `corpo.arranjo = "vertical"` é arranjo/composição, não ocupação de altura; registrar `ocupacao_vertical_terminal` (ou equivalente) como termo específico de preenchimento da altura da janela |
| `docs/contratos/contrato_tela_json.md` | Registrar altura disponível como dimensão futura da renderização da tela; registrar que o corpo deve preencher a área vertical disponível conforme ADR-0013 |
| `docs/contratos/contrato_composicao_corpo.md` | Registrar a diferença entre `corpo.arranjo = "vertical"` e ocupação vertical do terminal; registrar que o corpo pode ocupar a altura disponível com preenchimento de linhas em branco; registrar que a ocupação vertical não introduz novo arranjo nem altera composição |

### Arquivos que NÃO devem ser alterados por esta ADR

| Arquivo ou grupo | Motivo |
|---|---|
| `config/` | JSONs de produção permanecem; ocupação vertical é decisão de renderer, não de declaração |
| `tela/` | Implementação da altura dinâmica e do preenchimento vertical é pendência de handoff futuro |
| `docs/handoff/` | Artefatos históricos permanecem; handoff novo será criado no tempo próprio |
| `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md` | ADR aceita não é reescrita; sua semântica de `corpo.arranjo` é preservada |
| `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` | ADR aceita não é reescrita |

### Pendências derivadas

- Handoff futuro de implementação da ocupação vertical: propagar `.lines` do
  terminal até `renderizar_tela`, calcular `altura_disponivel` entre
  `cabecalho` e `barra_de_menus`, e implementar o preenchimento vertical do
  corpo.
- Decisão, no handoff de implementação, sobre a representação exata das
  linhas de preenchimento (linha visual interna à caixa do corpo vs. linha
  física com largura total).
- Casos de teste de altura disponível e de preenchimento vertical.

---

## Fora do escopo desta ADR

Os pontos abaixo não são decididos por esta ADR:

- **Implementar altura dinâmica no renderer ou na demo** — pendência de
  handoff futuro.
- **Decidir a representação final das linhas em branco no código** — linha
  visual interna vs. linha física total. Decisão de implementação adiada.
- **Alterar `corpo.arranjo`** — esta ADR não introduz nem remove valores de
  arranjo; `corpo.arranjo` permanece conforme ADR-0011.
- **Implementar `barra_de_menus.distribuicao = "horizontal"`** — conceito
  distinto, tratado pela ADR-0014.
- **Migrar `destino_minimo`** — fora de escopo explícito.
- **Resolver `sobreposto` residual** — fora de escopo explícito; aliases
  transicionais permanecem conforme ADR-0011.
- **Normatizar regra contra alteração por filtro parcial de texto** —
  tratada pela ADR-0014, Parte B.

---

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Tratar ocupação vertical como parte de ADR-0011 (`corpo.arranjo`) | Colapsa dois conceitos distintos (composição vs. ocupação da janela); perpetua ambiguidade da substring `vertical` |
| Não normatizar ocupação vertical e deixar como decisão do renderer | Deixa a decisão implícita; qualquer ADR futura sobre `arranjo vertical/horizontal` poderia ser lida ambiguamente e sobrescrever/acumular a decisão |
| Declarar ocupação vertical no `tela.json` | Quebra o princípio de que preenchimento vertical é responsabilidade do renderer; introduz estado de layout no JSON |
| Adiar a ADR até o handoff de implementação | A decisão é pré-requisito do handoff e da preservação terminológica frente a ADR-0014; adiar acumula risco de ambiguidade |

---

## Substituição parcial pela ADR-0024 (2026-07-15)

A **cláusula 4** desta ADR é **substituída pela ADR-0024** — Proibição de preenchimento vazio externo do corpo (2026-07-15).

**Trecho original — cláusula 4 (histórico, substituído):**

> "Quando o conteúdo funcional do corpo não ocupar toda a altura disponível, o renderer deve preencher o espaço restante com linhas em branco."

A ADR-0024 proíbe esse preenchimento externo vazio. A área não coberta por elementos visuais não pode ser preenchida pelo renderer com linhas em branco externas ao corpo. Qualquer formulação derivada desta cláusula 4 — incluindo as referências a "preenchimento de linhas em branco" nas consequências e pendências desta ADR — é substituída pela norma da ADR-0024.

**Partes que permanecem integralmente válidas:**

- **Cláusula 1** — a tela deve ocupar a largura e a altura disponíveis da janela do terminal.
- **Cláusula 2** — a altura deve passar a ser tratada como dimensão explícita do render.
- **Cláusula 3** — o corpo deve ocupar a `altura_disponivel` entre `cabecalho` e `barra_de_menus`.
- **Cláusula 5** — o preenchimento vertical é responsabilidade do renderer, não do JSON — agora restringido a garantir que elementos visuais ocupem toda a área.
- **Cláusulas 6, 7, 8, 9 e 10** — integralmente preservadas; a distinção entre `corpo.arranjo` e `ocupacao_vertical_terminal` permanece obrigatória.

**Nova norma complementar (ADR-0024):**

A obrigação de ocupação vertical da janela continua vigente (cláusula 1). A diferença é que essa ocupação deve ser concretizada por **elementos visuais** (`console`, `dashboard` ou `lancador`), não por linhas em branco externas inseridas pelo renderer. Toda a área física entre `cabecalho` e `barra_de_menus` deve pertencer à moldura de um elemento visual.

As regras DA-01 a DA-04 da ADR-0024 definem como essa ocupação integral é garantida:

- **DA-01 — Cardinalidade unitária**: quando houver exatamente um descendente visual, ele ocupa toda a área disponível mesmo sem `distribuicao` declarada.
- **DA-02 — Múltiplos elementos sem distribuição**: composição inválida quando dois ou mais elementos disputam o mesmo eixo sem `distribuicao`.
- **DA-03 — Grupos**: toda área atribuída a grupo ou container estrutural deve ser repassada integralmente aos descendentes visuais; grupo não justifica área vazia.
- **DA-04 — Invariante impossível**: composição que não satisfaz o invariante é rejeitada explicitamente, sem fallback silencioso.
