---
name: contrato-barra-de-menus
description: Schema e regras da barra_de_menus — região fixa de chips de ação da tela, distinta do objeto lancador do corpo
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#5-barra_de_menus"
    reaproveitado_de_legado: false
---

# Contrato — barra_de_menus

## 1. Objetivo

Especificar a `barra_de_menus`: sua natureza de região fixa da tela, a
taxonomia dos chips que ela contém, a ordem canônica desses chips, os três
tipos de propriedade dinâmica (existência, ativo/inativo, rótulo), e as
regras de uso que vinculam todos os renderers a esse contrato.

Este contrato cobre a seção 5 de `docs/NOMENCLATURA.md`. Estilo universal
(`contrato_estilo.md`, `ativo`) e composição de corpo
(`contrato_composicao_corpo.md`, `ativo`) são módulos separados e externos —
este contrato pode referenciá-los como dependências, mas não redefine nem
duplica suas regras.

---

## 2. Distinção fundamental — `barra_de_menus` vs objeto `lancador` do corpo

**`barra_de_menus`** e **`lancador`** são entidades completamente distintas.
Nenhum código, documentação ou nomenclatura pode usar os dois termos como
sinônimos ou de forma intercambiável.

| Conceito | O que é | Localização | Regido por |
|---|---|---|---|
| `barra_de_menus` | Região fixa da tela que contém os chips de ação e navegação | Sempre presente, separada do corpo | Este contrato |
| `lancador` | Tipo de objeto do corpo — composição de navegação dentro do próprio corpo da tela | Dentro do corpo, variável por tela | `contrato_lancador.md` |

**Consequências diretas desta distinção:**

- A `barra_de_menus` **não herda** nenhuma regra de distribuição, layout ou
  vãos do objeto `lancador` do corpo (`contrato_lancador.md`).
- Os arquivos de dados são separados:
  - `config/barra_de_menus.json` → dados concretos da `barra_de_menus`
  - `config/lancador.json` → parâmetros de layout do objeto `lancador` do corpo
- O termo `barra_de_menus` não pode ser abreviado para `barra_menu` — essa
  abreviação mistura dois termos distinguidos no glossário (ver
  `docs/NOMENCLATURA.md` seção 0).

---

## 3. Regra fundamental (formal, não observação)

**A `barra_de_menus` é um espelho, nunca uma fonte de decisão.**

Nenhum chip decide sua própria exibição. A existência de cada chip é sempre
derivada de uma propriedade de composição já declarada pela classe de tela.
O renderer da `barra_de_menus` lê a composição declarada, consulta a ordem
canônica em `config/barra_de_menus.json`, e exibe exatamente o que a classe
declarou — sem deliberação própria, sem lógica de seleção de chips, sem
fallback.

Esta regra deriva da seção 5.1 de `docs/NOMENCLATURA.md`, parágrafo "Regra
estrutural".

---

## 4. Fonte dos valores concretos

Todos os valores concretos da `barra_de_menus` — símbolos renderizáveis dos
chips, rótulos textuais finais, mapeamentos de tecla, materialização da ordem
canônica, mapeamento de cada chip para o eixo de composição que controla sua
existência, e condições de estado dinâmico — vivem em
**`config/barra_de_menus.json`**.

Este contrato define a **semântica**, as **regras** e os **invariantes**.
O JSON guarda os **valores**. Os dois artefatos têm responsabilidades separadas
e não sobrepostas (política da seção 0 de `docs/NOMENCLATURA.md`).

As notações entre colchetes usadas neste contrato, como `[Esc]`, `[<][>]`,
`[-][+]`, `[#]`, `[⇆]`, `[✥]`, `[␣]`, `[⏎]`, `[V]` e `[?]`, são
**identificadores semânticos/canônicos** dos chips e exemplos de referência
documental. Elas não são fonte normativa de renderização. O renderer deve ler
os valores renderizáveis concretos, rótulos textuais finais, símbolos finais e
mapeamentos de tecla em `config/barra_de_menus.json`.

O renderer deve ler `config/barra_de_menus.json` em tempo de execução. Nenhum
símbolo, rótulo ou ordem da `barra_de_menus` pode estar hardcoded no código.

---

## 5. Ordem canônica dos grupos de chips

A sequência abaixo define a posição relativa de cada chip ou grupo na
`barra_de_menus` como ordem semântica/canônica contratual. Sua materialização
concreta, incluindo os identificadores de dados e os valores renderizáveis, deve
ser lida de `config/barra_de_menus.json`.

```
[Esc] → [<][>] → [-][+] → [#] → [⇆] → [✥] → [␣] → [⏎] → específicos → [V] → [?]
```

A ordem é invariante: um chip condicional ausente naquela tela simplesmente
não ocupa espaço — os chips existentes mantêm a ordem relativa entre si.

---

## 6. Chips canônicos — semântica e regras de existência

### 6.1 Existência: estática vs dinâmica

A existência de um chip na `barra_de_menus` é uma propriedade **estática**,
derivada da composição declarada pela classe de tela. Ela não muda enquanto a
tela está aberta.

O estado **ativo/inativo** é uma propriedade **dinâmica**, recalculada a cada
render. Um chip inativo continua existindo na posição canônica — não desaparece.
O que muda é sua cor (usa `cor_inativo` do schema de estilo) e o fato de não
reagir a acionamento.

Esta distinção é definida em `docs/NOMENCLATURA.md` seção 1.5 e formalizada
em ADR-0004, que inclui `cor_inativo` e `cor_alerta` no schema de estilo
(`contrato_estilo.md` seção 3.5).

### 6.2 Chips de existência sempre presente

| Chip canônico / notação documental | Rótulo documental | Estado | Regra |
|---|---|---|---|
| `[Esc]` | Sair / Voltar / Limpar (ver seção 7) | sempre ativo | Primeiro na ordem; rótulo dinâmico conforme contexto |
| `[⏎]` | Todos / Executar / Visualizar (ver seção 8) | inativo sem alvo válido | Rótulo dinâmico conforme estado da seleção |
| `[?]` | Ajuda | sempre ativo | Último na ordem |

### 6.3 Chips de existência condicional

| Chip canônico / notação documental | Rótulo documental | Eixo de composição que condiciona existência | Notas de estado dinâmico |
|---|---|---|---|
| `[<][>]` | Páginas | `paginacao: com` | Inativo quando há apenas 1 página no momento |
| `[-][+]` | Colunas | `colunas_ajustavel: com` (tipo `console`) | `[-]` inativo em `n_col` mínimo; `[+]` inativo em `n_col` máximo pela largura atual |
| `[#]` | Grupos | `filtro_de_grupo: com` | Abre entrada para digitar número do grupo |
| `[⇆]` | Alternar | `quantidade_corpos: multiplos` | Move o foco de interação **entre corpos** — não confundir com `[✥]` |
| `[✥]` | Navegar | tela possui ao menos um corpo tipo `console` navegável | Ativo quando o corpo em foco é um corpo tipo `console` navegável; inativo via `cor_inativo` quando há corpo tipo `console` navegável na tela, mas o corpo em foco não é navegável por `[✥]` |
| `[␣]` | Selecionar | `formacao_de_selecao: com` | Toggle nomeado; indicador `incluido` do schema de estilo |
| `[V]` | Verboso | `tipo_exibicao: verboso` (tipo `console`) | — |
| específicos | (por classe) | definido por classe | Posicionados entre `[⏎]` e `[V]`/`[?]` |

Os rótulos documentais acima nomeiam a semântica dos chips neste contrato. Os
rótulos textuais finais e símbolos renderizados continuam sendo dados concretos
de `config/barra_de_menus.json`.

**`[✥]` — existência estrutural vs estado dinâmico**: a existência estrutural
de `[✥]` é estática e declarada pela classe/tela quando a tela possui ao menos
um corpo tipo `console` navegável. O chip não aparece/desaparece conforme o foco
atual, o dataset corrente ou o conteúdo renderizado naquele momento. Quando o
corpo em foco é um corpo tipo `console` navegável, `[✥]` fica ativo; quando o
corpo em foco não é navegável por `[✥]`, mas a tela possui outro corpo tipo
`console` navegável, `[✥]` permanece existente e pode ficar visualmente inativo
via `cor_inativo`. Se a tela não possui nenhum corpo tipo `console` navegável,
`[✥]` não existe.

**`[-][+]` — `n_col` não aparece no chip (decisão intencional)**: o chip
exibe o rótulo "Colunas"; o valor atual de `n_col` não aparece dentro do
chip. Essa ausência é decisão de design, não omissão; este contrato não
define outro local para exibir `n_col`.

**Distinção `[⇆]` vs `[✥]`**: `[⇆]` muda o foco de interação entre corpos
diferentes (nível da tela); `[✥]` move o cursor dentro do corpo que está em
foco no momento (nível do corpo). Não são intercambiáveis.

---

## 7. Comportamento contextual de `[Esc]`

`[Esc]` sempre existe e sempre está ativo, mas o rótulo e a ação variam
conforme o contexto da tela e o estado da seleção:

| Contexto | Rótulo documental | Ação |
|---|---|---|
| Há seleção ativa no corpo em foco | Limpar | Limpa a seleção; permanece na tela; só volta ao comportamento Sair/Voltar depois que a seleção for limpa |
| Sem seleção ativa, tela raiz (Orquestrador) | Sair | Encerra a sessão |
| Sem seleção ativa, qualquer outra tela | Voltar | Retorna à tela anterior |

A condição de "seleção ativa" é derivada do estado do corpo em foco — o renderer
consulta esse estado a cada render. A camada de limpeza tem precedência sobre a
de navegação: enquanto houver seleção, `[Esc]` sempre limpa, nunca navega.

---

## 8. Rótulo dinâmico de `[⏎]`

`[⏎]` sempre existe, mas o rótulo muda conforme o estado da tela:

| Estado | Rótulo documental | Ação |
|---|---|---|
| Tela com `formacao_de_selecao: com` e nada selecionado | Todos | Marca todos os itens do corpo; após isso o rótulo vira Executar |
| Alguma seleção marcada (manual ou via Todos) | Executar | Roda a função da tela sobre os itens selecionados |
| Tela de visualização sem execução | Visualizar | Abre o detalhe do item sob o cursor; não depende de seleção |

O rótulo dinâmico é recalculado a cada render. A regra de qual rótulo se aplica
vale para qualquer tela com `formacao_de_selecao: com` — não é tratamento
caso a caso por tela.

`[⏎]` fica **inativo** (usa `cor_inativo` do schema de estilo) quando não há
alvo válido sob o cursor.

---

## 9. Chips específicos — categoria formal

Chips específicos são declarados por cada classe de tela individualmente.
Três tipos formais estão definidos; um quarto tem estrutura pendente:

| Tipo | Natureza |
|---|---|
| **Toggle** | Filtro de exibição liga/desliga — estrutura: texto, tecla, `ativo` (booleano), papel |
| **Múltiplo** | Filtro de exibição em conjunto de opções, tipicamente mutuamente exclusivas — estrutura: texto, teclas (plural), cores por tecla, papel |
| **Aciona tela** | Abre outra tela (navegação) — estrutura: texto, tecla, `tela_destino`, papel; não executa lógica de fundo |
| **Aciona processo** | Executa lógica sobre seleção/lote — estrutura a definir (pendência registrada em `config/barra_de_menus.json` seção `_meta.pendencias`) |

Chips específicos sempre ocupam a posição entre `[⏎]` e `[V]`/`[?]` na ordem
canônica — nunca antes de `[⏎]` nem depois de `[?]`.

Em tela de processamento, ações próprias da classe são representadas por chips
específicos da `barra_de_menus`. Esses chips continuam na faixa canônica
definida acima, têm existência declarada pela classe de tela, e reforçam que a
`barra_de_menus` é espelho da composição declarada, não fonte de decisão.

Esta aplicação da ADR-0007 não define a estrutura do tipo específico
`aciona_processo`. `aciona_processo` permanece fora de escopo e pendente até
contrato próprio ou decisão específica.

Chips específicos de tela de processamento não transformam processamento em
tipo de corpo. Nenhuma regra de `[✥]` muda.

---

## 10. Estados visuais — relação com `contrato_estilo.md`

Os estados dinâmicos de cor dos chips são definidos pelo schema de estilo
universal (`contrato_estilo.md` seção 3.5):

| Estado | Campo do schema de estilo | Condição de aplicação |
|---|---|---|
| Inativo | `cor_inativo` | Chip existe (declarado), mas não está operável no estado atual |
| Alerta | `cor_alerta` | Valor atingiu limite ou exige destaque visual |

O renderer da `barra_de_menus` **não define** nem **hardcoda** cores de estado
dinâmico — lê exclusivamente do schema de estilo ativo. A tradução de nome
semântico de cor para valor de terminal é responsabilidade exclusiva do
renderer (R-7 de `contrato_estilo.md`).

Um chip com estado `cor_inativo` aplicado:
- continua ocupando sua posição na ordem canônica;
- não reage a acionamento do usuário;
- não desaparece da `barra_de_menus`.

---

## 11. Regras de uso

**R-1. Espelho puro.**
O renderer da `barra_de_menus` não possui lógica de decisão sobre quais chips
exibir. Lê a composição declarada pela classe e aplica as regras deste contrato.

**R-2. Proibição de hardcoding.**
Nenhum símbolo, rótulo, ordem ou condição de existência da `barra_de_menus`
pode estar hardcoded no código. Todos os valores concretos vêm de
`config/barra_de_menus.json`, lido em tempo de execução.

**R-3. Existência derivada de composição.**
A existência de qualquer chip condicional é derivada exclusivamente de um eixo
de composição declarado pela classe de tela. O renderer não inventa existência
com base em conteúdo dos dados, largura de terminal ou qualquer outra condição
de ambiente.

**R-4. Separação terminológica obrigatória.**
`barra_de_menus` e `lancador` nunca são usados como sinônimos — em código,
comentário ou documentação. `lancador` designa o tipo de objeto do corpo
(`contrato_lancador.md`); `barra_de_menus` designa a região fixa da tela
(este contrato). Sem herança de regras de layout entre os dois. O termo
`menu` permanece apenas como nome antigo/histórico do `lancador`.

**R-5. Separação de arquivos de dados.**
`config/barra_de_menus.json` e `config/lancador.json` não se substituem
nem se sobrepõem. Cada um serve seu domínio exclusivo.

**R-6. Estado dinâmico não remove chips.**
Um chip inativo permanece na posição canônica. Nunca é removido do layout por
estar inativo — apenas muda de cor e para de reagir a acionamento.

**R-7. Cores de estado dinâmico vêm do schema de estilo.**
O renderer consulta `cor_inativo` e `cor_alerta` do objeto de estilo ativo.
Não define valores de cor próprios para a `barra_de_menus`.

**R-8. Rótulo dinâmico de `[Esc]` tem precedência da seleção.**
Enquanto houver seleção ativa no corpo em foco, `[Esc]` sempre limpa a seleção
— nunca navega. O comportamento Sair/Voltar só se aplica depois que a seleção
for limpa ou quando não há seleção.

**R-9. Rótulo dinâmico de `[⏎]` é recalculado a cada render.**
O renderer determina o rótulo correto de `[⏎]` a cada render com base no
estado da tela — não guarda estado do rótulo entre renders.

**R-10. Chips específicos ficam dentro da faixa canônica.**
Chips específicos de classe nunca são posicionados fora da faixa entre `[⏎]`
e `[V]`/`[?]` na ordem canônica.

---

## 12. Critérios de validação

- [ ] Nenhum símbolo, rótulo ou posição de chip da `barra_de_menus` está
      hardcoded — todos os valores vêm de `config/barra_de_menus.json`.
- [ ] Um chip condicional ausente naquela tela não ocupa espaço na
      `barra_de_menus`; os chips existentes mantêm a ordem relativa canônica.
- [ ] Um chip inativo permanece na posição canônica, usa `cor_inativo` do
      schema de estilo ativo, e não reage a acionamento.
- [ ] `cor_inativo` e `cor_alerta` aplicadas ao chip vêm exclusivamente do
      schema de estilo ativo — nenhum valor de cor está hardcoded no renderer
      da `barra_de_menus`.
- [ ] `[Esc]` aplica a semântica documental de "Limpar" e limpa a seleção quando há seleção ativa
      no corpo em foco — independente do tipo de tela e da posição na hierarquia.
- [ ] `[Esc]` aplica a semântica documental de "Sair" apenas na tela raiz
      (Orquestrador) e sem seleção ativa; aplica "Voltar" em qualquer outra
      tela sem seleção ativa.
- [ ] `[⏎]` aplica a semântica documental de "Todos" quando
      `formacao_de_selecao: com` e nada está selecionado; "Executar" quando há
      seleção marcada; "Visualizar" em telas de visualização sem execução.
- [ ] `[⏎]` fica inativo (usa `cor_inativo`) quando não há alvo válido sob o
      cursor.
- [ ] `[<][>]` só existe quando `paginacao: com` está declarado pela classe;
      fica inativo quando o número de páginas é 1.
- [ ] `[-][+]` só existe quando `colunas_ajustavel: com` está declarado e o
      tipo de conteúdo é `console`; `[-]` inativo em `n_col` mínimo; `[+]` inativo
      em `n_col` máximo pela largura atual.
- [ ] `[⇆]` só existe quando `quantidade_corpos: multiplos` está declarado;
      move foco entre corpos, não cursor dentro do corpo.
- [ ] `[✥]` só existe estruturalmente quando a tela possui ao menos um corpo
      tipo `console` navegável — `lancador` e `dashboard` não contam como corpo
      navegável por `[✥]`; fica ativo quando o corpo em foco é um corpo tipo
      `console` navegável, inativo via `cor_inativo` quando o corpo em foco não é
      navegável por `[✥]`, sem aparecer/desaparecer por foco, dataset ou
      conteúdo corrente; se a tela não possui nenhum corpo tipo `console`
      navegável, `[✥]` não existe; as setas do teclado executam a navegação
      real quando ativo.
- [ ] `[␣]` só existe quando `formacao_de_selecao: com` está declarado.
- [ ] `[V]` só existe quando `tipo_exibicao: verboso` está disponível para
      corpo tipo `console`.
- [ ] Chips específicos de classe aparecem entre `[⏎]` e `[V]`/`[?]`.
- [ ] A distinção `barra_de_menus` vs objeto `lancador` do corpo é verificável:
      nenhuma regra de layout de `config/lancador.json` é consultada pelo
      renderer da `barra_de_menus`.
- [ ] `[?]` existe e está ativo em toda tela, sempre como último chip.

---

## 13. Pendências em aberto

Itens não bloqueantes para este contrato — herdados de
`docs/NOMENCLATURA.md` seção 11 e registrados em `config/barra_de_menus.json`:

- **Estrutura do chip específico tipo "aciona processo"**: lógica de execução
  ainda misturada com código de exibição no sistema legado — estrutura formal
  a definir quando o primeiro caso concreto for especificado.
- **Relação entre `[#]` (filtro de grupo) e `[␣]` (toggle de seleção)** quando
  ambos estão ativos simultaneamente: possibilidade de "marcar todos os itens
  do grupo filtrado" como atalho adiada intencionalmente para quando o caso de
  uso surgir.
