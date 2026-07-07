---
name: contrato-barra-de-menus
description: Schema e regras da barra_de_menus — região fixa inferior da tela; instância declarada no tela.json com lista de chips de ação; distinta do objeto lancador do corpo
metadata:
  type: contrato
  scope: scripts
  versao: "0.2"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#5-barra_de_menus"
    adrs_aplicadas:
      - docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md
      - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    reaproveitado_de_legado: false
---

# Contrato — barra_de_menus

## 1. Objetivo

Especificar a `barra_de_menus`: sua natureza de região fixa inferior da tela,
o modelo de instância declarada no `tela.json`, o schema e os invariantes que
definem o comportamento mínimo da região, a modelagem conceitual de chips como
entidades declarativas, a semântica e as regras de existência dos chips
canônicos, e as regras de uso que vinculam todos os renderers a este contrato.

O contrato define schema, invariantes e comportamento mínimo da região. A lista
concreta de chips, textos, teclas, ações, regras de existência e regras de
ativo/inativo vêm do `tela.json` da tela. O renderer valida e executa a
declaração sem hardcodar lista de chips, textos, teclas ou ações.

Este contrato prepara a modelagem futura de `chip` como classe própria
(DOC-B006), sem criar o contrato completo de `chip` nesta versão.

Este contrato cobre a seção 5 de `docs/NOMENCLATURA.md`. Estilo universal
(`contrato_estilo.md`, `ativo`) e composição de corpo
(`contrato_composicao_corpo.md`, `ativo`) são módulos separados e externos —
este contrato pode referenciá-los como dependências, mas não redefine nem
duplica suas regras. A fonte de autoridade sobre o schema de `tela.json` é
`contrato_tela_json.md`.

---

## 2. Natureza da `barra_de_menus`

`barra_de_menus` é a **região fixa inferior** de toda tela do sistema. Ela não
é parte do corpo, não é `lancador`, não é `cabecalho`.

Uma ocorrência concreta de `barra_de_menus` é uma **instância** declarada no
`tela.json` da tela. Esse modelo segue a ADR-0008: a instância concreta
pertence ao JSON da tela; o contrato define as regras do tipo.

| Conceito | O que é |
|---|---|
| Tipo `barra_de_menus` | Conjunto de regras, invariantes e comportamento mínimo — definido por este contrato |
| Instância de `barra_de_menus` | Região declarada no `tela.json` de uma tela; contém lista concreta de chips, regras de distribuição e parâmetros visuais da instância |

O renderer executa a instância conforme declarada e validada no `tela.json`.
Ele não decide lista de chips, textos, teclas, ações, regras de existência,
regras de ativo/inativo nem distribuição por conta própria.

A `barra_de_menus` não decide composição do corpo. Chips não determinam tipos,
arranjo ou presença de elementos no corpo. A `barra_de_menus` continua sendo
espelho da declaração da tela, não fonte de decisão.

---

## 3. Distinção fundamental — `barra_de_menus` vs objeto `lancador` do corpo

**`barra_de_menus`** e **`lancador`** são entidades completamente distintas.
Nenhum código, documentação ou nomenclatura pode usar os dois termos como
sinônimos ou de forma intercambiável.

| Conceito | O que é | Localização | Regido por |
|---|---|---|---|
| `barra_de_menus` | Região fixa inferior da tela que contém chips de ação | Sempre presente, separada do corpo | Este contrato |
| `lancador` | Tipo de elemento do corpo — composição de navegação dentro do corpo | Dentro do corpo, variável por tela | `contrato_lancador.md` |

**Consequências diretas desta distinção:**

- `lancador` **não herda** nenhuma regra da `barra_de_menus`.
- `barra_de_menus` **não herda** nenhuma regra de layout do `lancador`.
- Chips dos itens do `lancador` **não são** chips da `barra_de_menus` — são
  acionadores de navegação declarados no item; não pertencem à instância da
  barra.
- `barra_de_menus` fica **fora do corpo** — nunca é elemento de
  `corpo.elementos[]`.
- `barra_de_menus` **não decide** composição do corpo.
- O termo `barra_de_menus` não pode ser abreviado para `barra_menu` — essa
  abreviação mistura dois termos distinguidos no glossário (ver
  `docs/NOMENCLATURA.md` seção 0).

---

## 4. Regra fundamental

**A `barra_de_menus` é um espelho, nunca uma fonte de decisão.**

Nenhum chip decide sua própria exibição. A existência de cada chip é sempre
derivada de uma declaração no `tela.json` da tela. O renderer da
`barra_de_menus` lê a declaração da instância no `tela.json`, valida os chips
declarados e os exibe conforme as regras deste contrato — sem deliberação
própria, sem lógica de seleção de chips, sem fallback, sem lista hardcoded.

Esta regra deriva da seção 5.1 de `docs/NOMENCLATURA.md`, parágrafo "Regra
estrutural", e da ADR-0008.

---

## 5. Fonte dos valores concretos

A lista concreta de chips da `barra_de_menus` pertence ao `tela.json` da tela.
Regras concretas de chips da instância — textos, teclas, ações, regras de
existência, regras de ativo/inativo e forma de exibição — também pertencem ao
`tela.json`.

| Artefato | Responsabilidade |
|---|---|
| `tela.json` da tela | Lista concreta de chips, textos, teclas, ações, regras de existência, regras de ativo/inativo e parâmetros visuais da instância |
| `config/estilo.json` | Valores globais de aparência dos chips (presets de chip, `cor_inativo`, `cor_alerta`) |
| `config/barra_de_menus.json` | Artefato **ativo transicional** — a reavaliar/migrar conforme ADR-0008; não é mais a fonte universal definitiva dos valores concretos da instância |

As notações entre colchetes usadas neste contrato, como `[Esc]`, `[<][>]`,
`[-][+]`, `[#]`, `[⇆]`, `[✥]`, `[␣]`, `[⏎]`, `[V]` e `[?]`, são
**identificadores semânticos/canônicos** dos chips — **notação documental, não
normativa**. O renderer deve ler os valores renderizáveis concretos, rótulos
textuais finais, símbolos e mapeamentos de tecla do `tela.json`.

---

## 6. Chips como entidades declarativas

`tela.json` prepara a modelagem futura de `chip` como classe própria. Cada
chip declarado na instância da `barra_de_menus` deve poder declarar,
conceitualmente:

```text
id
tipo
tecla
texto
acao
regra_existencia
regra_ativo
forma_exibicao
```

**Tipos conceituais de chip** (não exaustivo; contrato de `chip` é pendência
DOC-B006):

```text
canonico    — chip padronizado com semântica contratual (ex.: [Esc], [⏎], [?])
especifico  — chip adicional declarado pela classe de tela
filtro      — chip que aciona filtro declarativo
alternancia — chip que alterna entre estados ou elementos (ex.: [⇆])
acao        — chip que aciona ação registrada
navegacao   — chip que aciona navegação entre telas
```

**Chips canônicos deixam de ser uma lista hardcoded.** Passam a ser instâncias
padronizadas: o contrato define a semântica, os invariantes e o comportamento
mínimo; a instância concreta é declarada no `tela.json`. Chips específicos são
instâncias adicionais declaradas pela classe de tela.

O contrato completo da classe `chip` será definido em tarefa posterior
(DOC-B006). Esta seção registra o modelo conceitual mínimo necessário para
guiar a declaração no `tela.json`.

---

## 7. Ordem canônica dos grupos de chips

A sequência abaixo define a posição relativa de cada chip ou grupo na
`barra_de_menus` como ordem semântica/canônica contratual. A lista concreta de
chips da instância é declarada no `tela.json`.

```
[Esc] → [<][>] → [-][+] → [#] → [⇆] → [✥] → [␣] → [⏎] → específicos → [V] → [?]
```

A ordem é invariante: um chip condicional ausente na instância simplesmente
não ocupa espaço — os chips existentes mantêm a ordem relativa entre si. O
renderer não inventa chips ausentes na declaração.

---

## 8. Chips canônicos — semântica e regras de existência

### 8.1 Existência: estática vs dinâmica

A existência de um chip na `barra_de_menus` é uma propriedade **estática**,
derivada da declaração no `tela.json`. Ela não muda enquanto a tela está aberta.

O estado **ativo/inativo** é uma propriedade **dinâmica**, recalculada a cada
render. Um chip inativo continua existindo na posição canônica — não desaparece.
O que muda é sua cor (usa `cor_inativo` do schema de estilo) e o fato de não
reagir a acionamento.

Esta distinção é definida em `docs/NOMENCLATURA.md` seção 1.5 e formalizada
em ADR-0004, que inclui `cor_inativo` e `cor_alerta` no schema de estilo
(`contrato_estilo.md` seção 3.5).

### 8.2 Chips canônicos de existência sempre presente

Os chips abaixo existem em toda instância de `barra_de_menus`. São chips
padronizados cuja semântica é definida por este contrato. A declaração
concreta no `tela.json` especifica texto, tecla e ação; os invariantes de
semântica são não negociáveis.

| Chip canônico / notação documental | Rótulo documental | Estado | Regra |
|---|---|---|---|
| `[Esc]` | Sair / Voltar / Limpar (ver seção 9) | sempre ativo | Primeiro na ordem; rótulo dinâmico conforme contexto |
| `[⏎]` | Ação do item em foco (ver seção 10) | inativo quando item em foco não tem ação válida | Rótulo derivado da ação declarada pelo item |
| `[?]` | Ajuda | sempre ativo | Último na ordem |

### 8.3 Chips canônicos de existência condicional

Os chips abaixo existem somente quando a instância de `console` ou a
configuração da tela declara a capacidade correspondente no `tela.json`.

| Chip canônico / notação documental | Rótulo documental | Condição de existência | Notas de estado dinâmico |
|---|---|---|---|
| `[<][>]` | Páginas | instância de `console` declara `paginacao: com` | Inativo quando há apenas 1 página no momento |
| `[-][+]` | Colunas | instância de `console` declara `colunas_ajustavel: com` | `[-]` inativo em `n_col` mínimo; `[+]` inativo em `n_col` máximo pela largura atual |
| `[#]` | Grupos | instância de `console` declara `filtro_de_grupo: com` | Chip de filtro declarativo — ver seção 13 |
| `[⇆]` | Alternar | tela declara múltiplos elementos de corpo | Move foco entre elementos de corpo — não confundir com `[✥]` (ver nota abaixo) |
| `[✥]` | Navegar | tela possui ao menos um `console` navegável — ver seção 11 | Ativo quando corpo em foco é `console` navegável; inativo via `cor_inativo` caso contrário |
| `[␣]` | Selecionar | instância de `console` declara seleção múltipla — ver seção 12 | Toggle por item selecionável |
| `[V]` | Verboso | instância de `console` permite modo verboso — ver seção 14 | Alterna modo verboso da instância |
| específicos | (por classe) | declarado pela classe de tela no `tela.json` | Posicionados entre `[⏎]` e `[V]`/`[?]` — ver seção 16 |

Os rótulos documentais acima nomeiam a semântica dos chips neste contrato. Os
rótulos textuais finais e formas de exibição são dados da instância declarada
no `tela.json`.

**`[-][+]` — `n_col` não aparece no chip (decisão intencional)**: o chip
exibe o rótulo de "Colunas"; o valor atual de `n_col` não aparece dentro do
chip. Essa ausência é decisão de design, não omissão.

**Distinção `[⇆]` vs `[✥]`**: `[⇆]` muda o foco de interação entre
elementos de corpo diferentes (nível da tela); `[✥]` move o cursor dentro
do elemento de corpo que está em foco no momento (nível do elemento).
Não são intercambiáveis.

---

## 9. `[Esc]` — comportamento contextual

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

## 10. `[⏎]` — ação por item

`[⏎]` representa a ação sobre o item em foco quando houver ação válida
declarada.

A ação pertence ao item e ao binding declarado no `tela.json`, não à tela
inteira de forma monolítica. Itens diferentes na mesma tela podem ter ações
diferentes, conforme suas declarações. O rótulo de `[⏎]` pode ser derivado
da ação declarada pelo item em foco, conforme contrato futuro de `chip`/ação
(DOC-B006).

| Estado do item em foco | Estado de `[⏎]` | Ação |
|---|---|---|
| Item tem ação válida declarada | ativo | Executa a ação declarada do item |
| Item sem ação declarada ou não acionável | inativo (usa `cor_inativo`) | Nenhuma ação |

**Semânticas documentais possíveis**: os três rótulos abaixo descrevem
semânticas que o `tela.json` pode mapear para ações de `[⏎]`. Não são
estados globais da tela — são exemplos de tipos de ação declarável por item:

| Semântica documental | Contexto típico |
|---|---|
| Todos | Tela com `formacao_de_selecao: com` e nada selecionado — ação que marca todos os itens; após isso o rótulo vira `Executar` |
| Executar | Seleção marcada — ação que executa a função sobre os itens selecionados |
| Visualizar | Tela de visualização sem execução — ação que abre o detalhe do item sob o cursor |

O rótulo concreto e o mapeamento de semântica para rótulo são dados da
instância declarada no `tela.json`. O renderer recalcula o estado e o rótulo
de `[⏎]` a cada render com base no item em foco e no estado atual da tela —
não guarda estado entre renders.

`[⏎]` fica **inativo** (usa `cor_inativo` do schema de estilo) quando não há
alvo válido sob o cursor ou quando o item em foco não tem ação declarada.

---

## 11. `[✥]` — navegação restrita a `console` navegável

`[✥]` existe estruturalmente somente quando a tela possui ao menos um elemento
de corpo do tipo `console` navegável.

**`[✥]` não navega `lancador`**: o `lancador` possui navegação própria por
itens via `tela_destino`, não é corpo navegável pelo cursor controlado pelas
setas do teclado (ADR-0005). O renderer da `barra_de_menus` não considera
`lancador` como condição de existência ou ativação de `[✥]`.

**`[✥]` não navega `dashboard`**: o `dashboard` é saída passiva não
interativa. Não expõe cursor navegável.

**Navegação ocorre por item, não por linha física**: quando `[✥]` está ativo,
as setas do teclado movem o cursor pelo `console` por unidade de item
navegável — não linha a linha do terminal.

A condição de existência e de ativação de `[✥]` considera somente `console`
navegável:

| Situação | Estado de `[✥]` |
|---|---|
| Tela não possui `console` navegável | `[✥]` não existe |
| Tela possui `console` navegável e o corpo em foco é esse `console` | `[✥]` ativo |
| Tela possui `console` navegável mas o corpo em foco não é `console` navegável | `[✥]` existe, mas inativo via `cor_inativo` |

O chip não aparece nem desaparece por foco, dataset corrente ou conteúdo
renderizado — sua existência é estática, derivada da declaração no `tela.json`.
O estado ativo/inativo é dinâmico.

---

## 12. `[␣]` — seleção múltipla por toggle

`[␣]` existe somente quando a instância de `console` declara seleção múltipla
(`formacao_de_selecao: multipla`).

**Seleção única não precisa de toggle**: quando a instância declara seleção
única (`unica`), o cursor define o item alvo — não há toggle. `[␣]` não
existe em instâncias com seleção única.

**Item deve ser selecionável**: o toggle de `[␣]` atua somente sobre itens
que declararem `selecionavel: true`. Item que não declara selecionabilidade
não participa do toggle e não muda de estado ao acionar `[␣]`.

---

## 13. Filtros declarativos

Filtros são chips declarativos que atuam sobre o conjunto exibido na instância
de `console`.

Regras:

- filtro atua no render, antes da paginação;
- filtro referencia campos existentes nos dados vinculados ao `console`
  declarado no `tela.json`;
- adicionar filtro sobre atributo já existente nos dados deve ser alteração
  declarativa no `tela.json` — sem alterar código de renderização;
- o renderer não pode conter lógica hardcoded de filtro específico; toda lógica
  de filtro é derivada da declaração no `tela.json`.

Estrutura conceitual do chip de filtro:

```text
chip
  tipo: filtro
  acao:
    tipo: alternar_filtro
    filtro: <id_do_filtro>
```

O filtro declarado referencia um filtro identificado no `tela.json`:

```text
filtros[]
  id
  campo
  tipo
  valores/opcoes
```

---

## 14. Modo verboso `[V]`

`[V]` alterna o modo verboso quando a instância de `console` permite.

Regras:

- `[V]` só existe quando a instância de `console` declara que aceita modo
  verboso;
- modo verboso é estado de exibição reutilizável — não é variação específica
  de cada tela;
- modo normal pode truncar itens com reticências conforme a política de
  overflow declarada pela instância;
- modo verboso permite que itens se expandam verticalmente conforme suas
  próprias regras internas de exibição declaradas;
- a tela não redefine a lógica interna de cada tipo de item em modo verboso.

---

## 15. Ações declarativas

Ações declaradas em chips no `tela.json` devem ser registradas/whitelisted.
O JSON nunca pode declarar comando arbitrário.

**Proibido conceitualmente:**

```json
{
  "acao": "python script_x.py --algo"
}
```

**Permitido conceitualmente:**

```json
{
  "acao": {
    "tipo": "abrir_tela",
    "alvo": "selecao"
  }
}
```

ou:

```json
{
  "acao": {
    "tipo": "executar_acao_registrada",
    "id": "atualizar_status"
  }
}
```

O renderer valida que toda ação declarada em chip pertence ao registro de
ações conhecidas. Ação não registrada é erro de validação — não é ignorada.

---

## 16. Chips específicos — categoria formal

Chips específicos são declarados por cada classe de tela individualmente no
`tela.json`. Três tipos formais estão definidos; um quarto tem estrutura
pendente:

| Tipo | Natureza |
|---|---|
| **Toggle** | Filtro de exibição liga/desliga — estrutura: texto, tecla, `ativo` (booleano), papel |
| **Múltiplo** | Filtro de exibição em conjunto de opções, tipicamente mutuamente exclusivas — estrutura: texto, teclas (plural), cores por tecla, papel |
| **Aciona tela** | Abre outra tela (navegação) — estrutura: texto, tecla, `tela_destino`, papel; não executa lógica de fundo |
| **Aciona processo** | Executa lógica sobre seleção/lote — estrutura a definir (pendência DOC-B006) |

Chips específicos sempre ocupam a posição entre `[⏎]` e `[V]`/`[?]` na ordem
canônica — nunca antes de `[⏎]` nem depois de `[?]`.

Em tela de processamento, ações próprias da classe são representadas por chips
específicos declarados no `tela.json`. Esses chips têm existência declarada
pela classe de tela; a `barra_de_menus` continua sendo espelho da declaração,
não fonte de decisão. Chips específicos de tela de processamento não
transformam processamento em tipo de corpo. Nenhuma regra de `[✥]` muda.

---

## 17. Distribuição e ordem de instância

A instância da `barra_de_menus` declarada no `tela.json` determina:

- lista concreta de chips;
- regra de distribuição dos chips na região;
- parâmetros visuais locais da instância.

Regras de distribuição:

- o renderer não inventa chips ausentes — chips não declarados na instância
  não ocupam espaço;
- chips inativos continuam visíveis quando a regra da instância assim
  determinar;
- a ordem relativa canônica definida na seção 7 é invariante entre os chips
  existentes na instância — chips presentes respeitam a sequência canônica;
- teclas duplicadas na mesma instância da `barra_de_menus` são erro de
  validação.

---

## 18. Estados visuais — relação com `contrato_estilo.md`

Os estados dinâmicos de cor dos chips são definidos pelo schema de estilo
universal (`contrato_estilo.md` seção 3.5):

| Estado | Campo do schema de estilo | Condição de aplicação |
|---|---|---|
| Inativo | `cor_inativo` | Chip existe (declarado), mas não está operável no estado atual |
| Alerta | `cor_alerta` | Valor atingiu limite ou exige destaque visual |

O renderer da `barra_de_menus` **não define** nem **hardcoda** cores de estado
dinâmico — lê exclusivamente do schema de estilo ativo. A tradução de nome
semântico de cor para valor de terminal é responsabilidade exclusiva do renderer.

Um chip com estado `cor_inativo` aplicado:
- continua ocupando sua posição na ordem canônica;
- não reage a acionamento do usuário;
- não desaparece da `barra_de_menus`.

---

## 19. Regras de uso

**R-1. Espelho puro.**
O renderer da `barra_de_menus` não possui lógica de decisão sobre quais chips
exibir. Lê a declaração da instância no `tela.json`, valida e aplica as regras
deste contrato. Não possui fallback nem inventa chips ausentes.

**R-2. Proibição de hardcoding.**
Nenhum chip, símbolo, rótulo, tecla, ação, ordem, regra de existência nem
regra de ativo/inativo da `barra_de_menus` pode estar hardcoded no código.
O renderer percorre `chips[]` da instância declarada no `tela.json`.

**R-3. Existência derivada de declaração no `tela.json`.**
A existência de qualquer chip condicional é derivada exclusivamente da
declaração no `tela.json`. O renderer não inventa existência com base em
conteúdo dos dados, largura de terminal ou qualquer outra condição de ambiente.

**R-4. Separação terminológica obrigatória.**
`barra_de_menus` e `lancador` nunca são usados como sinônimos — em código,
comentário ou documentação. Sem herança de regras de layout entre os dois.
O termo `menu` permanece apenas como nome antigo/histórico do `lancador`.

**R-5. Separação de responsabilidade de artefatos.**
`tela.json` é a fonte dos dados concretos da instância. `config/estilo.json`
é a fonte de aparência global. `config/barra_de_menus.json` é artefato ativo
transicional a reavaliar conforme ADR-0008.

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

**R-9. Estado e rótulo de `[⏎]` são recalculados a cada render.**
O renderer determina o estado e o rótulo de `[⏎]` a cada render com base no
item em foco e no estado da tela — não guarda estado entre renders. A ação
pertence ao item/binding, não à tela de forma monolítica.

**R-10. Chips específicos ficam dentro da faixa canônica.**
Chips específicos de classe nunca são posicionados fora da faixa entre `[⏎]`
e `[V]`/`[?]` na ordem canônica.

**R-11. Ações declaradas em chips são whitelisted.**
O renderer valida que toda ação declarada em chip pertence ao registro de ações
conhecidas. Ação não registrada é erro de validação — não é ignorada nem
executada.

**R-12. `[✥]` não navega `lancador` nem `dashboard`.**
O chip `[✥]` e as setas do teclado controlam somente cursor de `console`
navegável. `lancador` e `dashboard` não participam da condição de existência
nem de ativação de `[✥]` (ADR-0005).

---

## 20. Critérios de validação

- [ ] A instância da `barra_de_menus` possui `chips[]` declarados — instância
      sem chips é inválida, salvo exceção futura documentada.
- [ ] Todo chip declarado tem `id` — chip sem `id` é inválido.
- [ ] Todo chip acionável tem `tecla` — chip sem `tecla` é inválido, salvo
      chip puramente visual explicitamente permitido no futuro.
- [ ] Todo chip acionável tem `texto` — chip sem `texto` é inválido, salvo
      exceção futura documentada.
- [ ] Todo chip acionável tem `acao` ou regra associada declarada — chip acionável
      sem ação é inválido.
- [ ] Teclas duplicadas na mesma instância da `barra_de_menus` são erro de
      validação.
- [ ] Toda ação declarada em chip pertence ao registro de ações conhecidas —
      ação não registrada é erro de validação.
- [ ] Filtro referenciado por chip de filtro existe na declaração da tela.
- [ ] `[✥]` não pode ser vinculado a `lancador` nem a `dashboard`.
- [ ] `[␣]` não pode existir se a instância de `console` não declarar seleção
      múltipla.
- [ ] `[⏎]` calcula ativo/inativo conforme o item em foco: ativo quando o
      item tem ação válida declarada, inativo quando o item em foco não tem
      ação declarada ou não há alvo válido.
- [ ] O renderer não pode hardcodar chip, texto, tecla, ação, regra de
      existência ou regra de estado — todos os valores vêm do `tela.json`.
- [ ] Um chip condicional ausente na declaração da tela não ocupa espaço na
      `barra_de_menus`; os chips existentes mantêm a ordem relativa canônica.
- [ ] Um chip inativo permanece na posição canônica, usa `cor_inativo` do schema
      de estilo ativo, e não reage a acionamento.
- [ ] `cor_inativo` e `cor_alerta` aplicadas ao chip vêm exclusivamente do schema
      de estilo ativo — nenhum valor de cor está hardcoded no renderer.
- [ ] `[Esc]` aplica a semântica de "Limpar" quando há seleção ativa no corpo
      em foco — independente do tipo de tela.
- [ ] `[Esc]` aplica "Sair" apenas na tela raiz sem seleção ativa; "Voltar"
      em qualquer outra tela sem seleção ativa.
- [ ] `[⏎]` fica inativo (usa `cor_inativo`) quando não há alvo válido ou
      quando o item em foco não tem ação declarada.
- [ ] `[<][>]` só existe quando a instância de `console` declara `paginacao:
      com`; fica inativo quando o número de páginas é 1.
- [ ] `[-][+]` só existe quando a instância de `console` declara
      `colunas_ajustavel: com`; `[-]` inativo em `n_col` mínimo; `[+]`
      inativo em `n_col` máximo pela largura atual.
- [ ] `[⇆]` só existe quando a tela declara múltiplos elementos de corpo;
      move foco entre elementos, não cursor dentro do elemento.
- [ ] `[✥]` só existe quando a tela declara ao menos um `console` navegável;
      `lancador` e `dashboard` não contam; ativo quando o corpo em foco é
      `console` navegável, inativo via `cor_inativo` caso contrário; não
      aparece/desaparece por foco, dataset ou conteúdo corrente.
- [ ] `[␣]` só existe quando a instância de `console` declara seleção múltipla;
      atua somente sobre itens que declararem `selecionavel: true`.
- [ ] `[V]` só existe quando a instância de `console` declara que permite modo
      verboso.
- [ ] Chips específicos de classe aparecem entre `[⏎]` e `[V]`/`[?]`.
- [ ] `[?]` existe e está ativo em toda instância da `barra_de_menus`, sempre
      como último chip.
- [ ] A distinção `barra_de_menus` vs objeto `lancador` do corpo é verificável:
      chips dos itens do `lancador` não são chips da `barra_de_menus`; nenhuma
      regra de layout de `contrato_lancador.md` é aplicada ao renderer da barra.

---

## 21. Pendências em aberto

- **Contrato/classe `chip`** (DOC-B006): a modelagem conceitual introduzida
  neste contrato (seção 6) deve ser formalizada em contrato próprio. Campos
  obrigatórios, tipos formais, ações whitelisted, regras de existência e regras
  de ativo/inativo precisam ser fechados antes da implementação.

- **Estrutura do chip específico tipo "aciona processo"**: estrutura formal a
  definir quando o primeiro caso concreto for especificado.

- **Relação entre `[#]` (filtro de grupo) e `[␣]` (toggle de seleção)** quando
  ambos estão ativos simultaneamente: possibilidade de "marcar todos os itens
  do grupo filtrado" como atalho adiada intencionalmente para quando o caso de
  uso surgir.

- **`config/barra_de_menus.json` como artefato transicional**: a reavaliar e
  migrar para o modelo de configuração por tela (ADR-0008) em tarefa posterior.
