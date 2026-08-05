---
name: contrato-barra-de-menus
description: Schema e regras da barra_de_menus — região fixa inferior da tela; instância declarada no tela.json com lista de chips de ação; distinta do objeto lancador do corpo
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.2"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md"
    adrs_aplicadas:
      - docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md
      - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
      - docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
      - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
      - docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md
      - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
      - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
      - docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
    reaproveitado_de_legado: false
  dependencias_nomenclatura:
    dependencias_obrigatorias:
      - docs/nomenclatura/01_NUCLEO_COMUM.md
      - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    dependencias_condicionais:
      - modulo: docs/nomenclatura/10_ESTILO.md
        quando: tratar estado ou apresentação visual dos chips
      - modulo: docs/nomenclatura/32_CONSOLE.md
        quando: tratar chips ligados a console
      - modulo: docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
        quando: tratar chip [V] Verboso ou política de modo (D23)
      - modulo: docs/nomenclatura/90_ALIASES_E_TERMOS_DESCONTINUADOS.md
        quando: houver termo transicional
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

Este contrato cobre a terminologia de `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`. Estilo universal
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
  `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`).

---

## 4. Regra fundamental

**A `barra_de_menus` é um espelho, nunca uma fonte de decisão.**

Nenhum chip decide sua própria exibição. A existência de cada chip é sempre
derivada de uma declaração no `tela.json` da tela. O renderer da
`barra_de_menus` lê a declaração da instância no `tela.json`, valida os chips
declarados e os exibe conforme as regras deste contrato — sem deliberação
própria, sem lógica de seleção de chips, sem fallback, sem lista hardcoded.

Esta regra deriva de `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
(regra estrutural) e da ADR-0008.

**Política declarativa por tela (ADR-0012, 2026-07-08)**: a `barra_de_menus`
é declarativa por tela e **não contém todos os chips canônicos por padrão**.
Cada tela declara apenas os chips aplicáveis ao seu estado/capacidade atual.
O Orquestrador não precisa declarar todos os chips canônicos. A existência de
um chip canônico como categoria semântica **não obriga** sua presença em toda
tela — "canônico" define semântica e ordem quando o chip está presente, não
obrigatoriedade de declaração. Chips condicionais só devem ser declarados
quando a capacidade correspondente existir ou for aplicável à tela; se a
capacidade não está implementada, o chip não deve ser declarado apenas por
ser canônico. Testes devem validar os chips declarados no JSON da tela, não
um conjunto global obrigatório.

**Barra mínima da tela real inicial (ADR-0022, 2026-07-14)**: a futura tela
inicial real `orquestrador` deverá declarar, no mínimo, `Esc`, `?` e acesso a
estilos. Essa regra é específica da instância `config/telas/orquestrador.json`
e não transforma esses itens em lista global obrigatória para toda tela. O
item de estilos deverá permanecer sem navegação para destino inexistente até
que a tela funcional de estilos seja decidida e implementada por ciclo próprio.

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
| `config/elementos/barra_de_menus.json` | Futuro caminho do artefato **ativo transicional** — a reavaliar/migrar conforme ADR-0008 e ADR-0021; não é mais a fonte universal definitiva dos valores concretos da instância |

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
alternancia — chip que alterna estados ou foco entre consoles focalizáveis (ex.: [⇆])
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

Esta distinção é definida em `docs/nomenclatura/10_ESTILO.md` e formalizada
em ADR-0004, que inclui `cor_inativo` e `cor_alerta` no schema de estilo
(`contrato_estilo.md` seção 3.5).

### 8.2 Chips canônicos de semântica fixa

Os chips abaixo são canônicos de semântica fixa. "Canônico" significa
nome/semântica reconhecida pelo sistema, **não** presença obrigatória em toda
tela (ADR-0012). A presença de cada um é declarativa por tela: a instância
declarada no `tela.json` declara apenas os chips aplicáveis ao seu
estado/capacidade atual. Quando presentes, esses chips seguem os invariantes
contratuais abaixo (posição e estado); a declaração concreta no `tela.json`
especifica texto, tecla e ação, e os invariantes de semântica são não
negociáveis.

| Chip canônico / notação documental | Rótulo documental | Estado (quando presente) | Regra |
|---|---|---|---|
| `[Esc]` | Sair / Voltar / Limpar (ver seção 9) | sempre ativo | Primeiro na ordem quando declarado; rótulo dinâmico conforme contexto |
| `[⏎]` | Ação do item em foco (ver seção 10) | inativo quando item em foco não tem ação válida | Rótulo derivado da ação declarada pelo item |
| `[?]` | Ajuda | sempre ativo | Último na ordem quando declarado |

### 8.3 Chips canônicos de existência condicional

Os chips abaixo existem somente quando a instância de `console` ou a
configuração da tela declara a capacidade correspondente no `tela.json`.

| Chip canônico / notação documental | Rótulo documental | Condição de existência | Notas de estado dinâmico |
|---|---|---|---|
| `[<][>]` | Páginas | instância de `console` declara `paginacao: com` | Topologia limitada, sem wrap entre primeira e última página (ADR-0038 D-PAG-01); inativo quando há apenas 1 página no momento, inclusive com conjunto vazio (`página 1/1`); estado calculado pela página do console focado — ver seção 24 |
| `[-][+]` | Colunas | instância de `console` declara `colunas_ajustavel: com` | `[-]` inativo em `n_col` mínimo; `[+]` inativo em `n_col` máximo pela largura atual |
| `[#]` | Grupos | instância de `console` declara `filtro_de_grupo: com` | Chip de filtro declarativo — ver seção 13 |
| `[⇆]` | Alternar | tela possui pelo menos dois consoles focalizáveis (ADR-0031 D14) | Move foco entre consoles focalizáveis — não confundir com `[✥]` (ver nota abaixo e seção 20) |
| `[✥]` | Navegar | console focado possui mais de um item navegável (ADR-0031 D14) — ver seção 11 e seção 20 | Ausente quando não há console focado, quando o console tem zero itens ou um único item navegável |
| `[␣]` | Selecionar | instância de `console` declara seleção múltipla — ver seção 12 | Toggle por item selecionável |
| `[V]` | Verboso | instância de `console` permite modo verboso — ver seção 14 | Alterna modo verboso da instância |
| específicos | (por classe) | declarado pela classe de tela no `tela.json` | Posicionados entre `[⏎]` e `[V]`/`[?]` — ver seção 16 |

Os rótulos documentais acima nomeiam a semântica dos chips neste contrato. Os
rótulos textuais finais e formas de exibição são dados da instância declarada
no `tela.json`.

**`[-][+]` — `n_col` não aparece no chip (decisão intencional)**: o chip
exibe o rótulo de "Colunas"; o valor atual de `n_col` não aparece dentro do
chip. Essa ausência é decisão de design, não omissão.

**Distinção `[⇆]` vs `[✥]`**: `[⇆]` muda o foco de interação entre consoles
focalizáveis (nível da tela); `[✥]` move o cursor entre itens do console
focado (nível do console). Grupos estruturais, `dashboard`, `lancador`,
console não navegável e console navegável sem itens navegáveis não contam para
`[⇆]`. Não são intercambiáveis.

---

## 9. `[Esc]` — comportamento contextual

`[Esc]`, quando declarado na instância, é sempre ativo, mas o rótulo e a ação
variam conforme o contexto da tela e o estado da seleção:

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

## 11. `[✥]` — navegação restrita ao console focado

`[✥]` aparece somente quando existe console focado e esse console possui mais
de um item navegável. O chip fica ausente quando a navegação pelas setas não
pode produzir movimento.

**`[✥]` não navega `lancador`**: o `lancador` possui navegação própria por
itens via `tela_destino`, não é corpo navegável pelo cursor controlado pelas
setas do teclado (ADR-0005). O renderer da `barra_de_menus` não considera
`lancador` como condição de existência ou ativação de `[✥]`.

**`[✥]` não navega `dashboard`**: o `dashboard` é saída passiva não
interativa. Não expõe cursor navegável.

**Navegação ocorre por item, não por linha física**: quando `[✥]` está presente,
as setas do teclado movem o cursor pelo `console` por unidade de item
navegável — não linha a linha do terminal.

A condição de presença de `[✥]` é dinâmica e considera o console focado:

| Situação | Presença de `[✥]` |
|---|---|
| Não existe console focado | `[✥]` ausente |
| Console focado não possui itens navegáveis | `[✥]` ausente |
| Console focado possui exatamente um item navegável | `[✥]` ausente |
| Console focado possui mais de um item navegável | `[✥]` presente |

```yaml
chip_setas:
  aparece_quando:
    - existe_console_focado
    - console_focado_possui_mais_de_um_item_navegavel

  nao_aparece_quando:
    - nao_existe_console_focado
    - console_focado_nao_possui_itens_navegaveis
    - console_focado_possui_exatamente_um_item_navegavel

  estado_inativo_sem_movimento: nao_utilizado
```

Para `[✥]`, não se usa estado inativo sem movimento: ou o chip está presente
porque as setas podem mover o cursor entre itens, ou está ausente.

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

### 16.1 Acesso a estilos na tela real inicial

Pela ADR-0022, o acesso a estilos da tela inicial real é item específico da
instância `orquestrador`. Ele deve estar visível desde a tela inicial real,
mas não autoriza criar tela funcional de estilos, destino inexistente, ação
temporária, fallback para demonstração, troca de borda, troca de envelope de
chips ou persistência de seleção de estilo.

Enquanto a tela funcional correspondente não existir, o item de estilos deve
ser inicialmente declarativo e não navegável somente se os contratos ativos
permitirem essa forma. Se a validação vigente exigir ação ou `tela_destino`
existente para todo item visível, a criação física da tela real deverá
aguardar decisão adicional do usuário.

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

**Distribuição horizontal responsiva (ADR-0014, 2026-07-09)**:
`barra_de_menus.distribuicao` é termo específico completo que controla a
disposição visual dos chips na região da barra.

- `barra_de_menus.distribuicao = "horizontal"` **NÃO** significa linha única
  fixa; significa **distribuição horizontal responsiva** dos chips.
- `barra_de_menus.distribuicao = "horizontal"` é **alias transitório** de
  `barra_de_menus.distribuicao.modo = "horizontal_responsiva"`, com defaults
  definidos por este contrato ou pelo handoff aplicável.
- O **formato canônico futuro** de `barra_de_menus.distribuicao` é **objeto
  declarativo** com `modo = "horizontal_responsiva"` (a migração de
  JSON/código/testes para esse formato é pendência de handoff futuro; este
  contrato não cria nem altera JSON).
- **Tentativa inicial** em linha única (`tentativa_inicial = "linha_unica"`).
- **Quebra** para multilinha quando não couber
  (`quebra = "multilinha_quando_nao_couber"`), até `linhas.maximo`.
- **Preenchimento multilinha** declarado (`coluna_a_coluna` ou
  `linha_a_linha`).
- **Vãos** mínimos/máximos declarados (`margem_horizontal`, `vao_chip_texto`,
  `vao_entre_chips`, `vao_entre_colunas`, `vao_vertical_entre_linhas`).
- **Ordem** por declaração (`ordem.politica = "declaracao"` usa a ordem de
  `barra_de_menus.chips[]`; `"grupos_declarados"` usa a ordem dos grupos e
  dos chips dentro de cada grupo).
- **Âncoras** (ex.: `chip_esc` primeiro, `chip_ajuda` último) são restrições
  de **validação**, não instruções de reordenação automática; ordem que
  viola âncora é erro de validação, o renderer não reordena para corrigir.
- **Overflow** determinístico: quando nenhum arranjo couber, o resultado é
  `quando_nao_couber = "erro_layout"` — erro determinístico de layout, nunca
  omissão/truncamento/reordenação para "fazer caber".

**Proibições do renderer** (reforçam a seção 19 e a ADR-0014):

- **não empilhar um chip por linha** como fallback quando a distribuição
  declarada for `horizontal`/`horizontal_responsiva`;
- **não omitir chip** quando não couber (`nao_omitir_chips`);
- **não truncar texto** para caber (`nao_truncar_texto`);
- **não reordenar chips** para caber (`nao_reordenar`);
- **não inventar chips ausentes** nem completar a barra com a lista
  canônica global;
- **não aplicar regra do `lancador` por herança** — a distribuição da barra
  é independente da composição do corpo.

A distribuição horizontal responsiva da barra **não é** o mesmo conceito que
`corpo.arranjo = "horizontal"` (arranjo do corpo, ADR-0011): são campos em
regiões distintas com semântica própria e independentes entre si. Chips de
itens do `lancador`/corpo (ex.: `g`, `d`) não são chips da `barra_de_menus` e
não seguem esta distribuição. A implementação da distribuição horizontal
responsiva no renderer é pendência de handoff futuro; esta seção fixa a norma
contratual que o handoff deverá respeitar.

---

## 18. Estados visuais — relação com `contrato_estilo.md`

Os estados dinâmicos de cor dos chips são definidos pelo schema de estilo
universal (`contrato_estilo.md` seção 3.5):

| Estado | Campo do schema de estilo | Condição de aplicação |
|---|---|---|
| Inativo | `cor_inativo` | Chip existe (declarado), mas não está operável no estado atual |
| Alerta / destaque | `cor_alerta` | Elemento operável em destaque, ou valor/limite que exige atenção |

O renderer da `barra_de_menus` **não define** nem **hardcoda** cores de estado
dinâmico — lê exclusivamente do schema de estilo ativo. A tradução de nome
semântico de cor para valor de terminal é responsabilidade exclusiva do renderer.

Um chip com estado `cor_inativo` aplicado:
- continua ocupando sua posição na ordem canônica;
- não reage a acionamento do usuário;
- não desaparece da `barra_de_menus`.

Um chip com `cor_alerta` aplicado permanece operável: destaque não implica
inatividade (ADR-0037).

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
é a fonte de aparência global. `config/elementos/barra_de_menus.json` é o
futuro caminho do artefato ativo transicional a reavaliar conforme ADR-0008 e
ADR-0021.

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
- [ ] `[⇆]` só existe quando a tela possui pelo menos dois consoles
      focalizáveis (ADR-0031 D14); consoles sem itens navegáveis não contam;
      move foco entre consoles, não cursor dentro do console.
- [ ] `[✥]` aparece somente quando o console focado possui mais de um item
      navegável (ADR-0031 D14); ausente quando não há console focado, quando
      o console tem zero itens navegáveis ou quando tem exatamente um item
      navegável; `lancador` e `dashboard` não entram na condição. Em console
      paginado, a condição considera somente os itens navegáveis da página
      atual (ADR-0038 D-PAG-04).
- [ ] `[<]` fica inativo na primeira página e `[>]` fica inativo na última;
      ambos ficam inativos quando há somente uma página (`página 1/1`),
      inclusive com conjunto vazio; não há paginação circular entre primeira
      e última página (ADR-0038 D-PAG-01, D-PAG-11, D-PAG-12).
- [ ] O estado de `[<][>]` é calculado a partir da página do console focado;
      sem console focado, ou com o console focado sem `paginacao: com`
      declarada, ambos ficam inativos; os comandos de página não alteram a
      página de nenhum outro console nem o foco corrente (ADR-0038 D-PAG-13).
- [ ] As entradas aceitas para página anterior são `,` e `<`; para próxima
      página, `.` e `>` (ADR-0038 D-PAG-14).
- [ ] `[␣]` só existe quando a instância de `console` declara seleção múltipla;
      atua somente sobre itens que declararem `selecionavel: true`.
- [ ] `[V]` só existe quando a instância de `console` declara que permite modo
      verboso.
- [ ] Chips específicos de classe aparecem entre `[⏎]` e `[V]`/`[?]`.
- [ ] O controle universal `[Ins]` só existe quando a tela declara
      validamente `controle_execucao.modo_inicial` e satisfaz a compatibilidade
      integral das ações de processo relevantes com `executar` e `dry_run`.
- [ ] A ausência de `controle_execucao` deixa o chip universal ausente.
- [ ] O controle universal permanece ativo nos dois estados, usa o rótulo
      correspondente ao modo corrente (`Real`/`Simulação`, D-DRY-12) e aplica
      `cor_alerta` somente em `Simulação`.
- [ ] `[?]`, quando declarado, é o último chip da instância e permanece ativo.
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

- **`config/elementos/barra_de_menus.json` como artefato transicional**: a
  reavaliar e migrar para o modelo de configuração por tela (ADR-0008) em
  tarefa posterior, preservada a organização prevista pela ADR-0021.

---

## 22. Chip `[V] Verboso` nas demonstrações de conteúdo multinível do console (ADR-0028)

A ADR-0028 (2026-07-17) formaliza a semântica da tecla `V` e do chip
`[V] Verboso` para instâncias de `console` com conteúdo multinível externo.

### 22.1 Existência condicional

O chip `[V] Verboso` existe apenas quando a instância de `console` apresenta
dados multinível externos e declara a política de modo `"alternavel"` no campo
`formato.excesso.politica_modo` do JSON estrutural da tela (D23).

Telas com política `"somente_verboso"` ou `"somente_nao_verboso"` não exibem o
chip `[V] Verboso` e não expõem a tecla `V` como ação aplicável.

A existência do chip é derivada exclusivamente da política declarada no
`tela.json`. O renderer não infere a política a partir do conteúdo externo nem
de outra condição de ambiente.

### 22.2 Semântica da alternância

A ativação de `[V]`:

- alterna o estado de visualização entre verboso e não verboso;
- usa os mesmos dados, a mesma tela e o mesmo documento de conteúdo;
- não troca a apresentação;
- não persiste alteração;
- é reversível: uma segunda ativação retorna ao modo anterior.

### 22.3 Estado de sessão

O estado verboso/não verboso é estado da sessão. Ele não é gravado no JSON
externo de conteúdo, no JSON estrutural da tela nem em nenhum arquivo.

Ao recarregar a tela ou trocar de cenário, o modo inicial volta a ser determinado
pela política de modo declarada no JSON estrutural da tela
(`formato.excesso.politica_modo` e, para telas alternáveis,
`formato.excesso.modo_inicial`).

### 22.4 Isolamento

A ativação de `[V]` em uma instância de `console` com dados multinível:

- não vaza para outra instância de `console`;
- não altera a identidade do cenário;
- não persiste preferência global.

### 22.5 Inaplicabilidade fora do escopo

O chip `[V]` desta seção aplica-se exclusivamente às demonstrações de conteúdo
multinível do `console`. Ele não se aplica a:

- `dashboard`;
- `lancador`;
- `console` sem conteúdo multinível externo;
- distribuição matricial de nível único.

### 22.6 Posição canônica

O chip `[V] Verboso` das demonstrações de conteúdo multinível do `console`
ocupa a mesma posição canônica já definida pela seção 7 deste contrato — após
os chips específicos de classe e antes de `[?]`.

### 22.7 Remissões

- `contrato_console.md` — seção 21 (ADR-0028): estado de visualização, alternância e políticas de modo;
- `contrato_json_console.md` — seção 13 (ADR-0028): regras normativas, validações e política de modo;
- `contrato_tela_json.md` — seção 33 (ADR-0028): JSON estrutural e declaração de política;
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` — terminologia canônica da ADR-0028.

### 22.8 Três políticas de modo e o chip `[V] Verboso` (D23)

A revisão D23 da ADR-0028 distingue três políticas de modo para telas de `console`
multinível. A presença ou ausência do chip `[V] Verboso` é determinada pela
política declarada no JSON estrutural (`formato.excesso.politica_modo`):

| Política (`politica_modo`) | Chip `[V] Verboso` | Tecla `V` |
|---|---|---|
| `"somente_verboso"` | Não obrigatório | Não aplicável |
| `"somente_nao_verboso"` | Não obrigatório | Não aplicável |
| `"alternavel"` | **Obrigatório** | Ativa alternância |

O chip representa a **disponibilidade de alternância**, não o modo corrente nem a
política por si só. Em telas alternáveis, o chip é sempre exibido,
independentemente de o estado corrente da sessão ser verboso ou não verboso.

Telas de modo único não necessitam do chip. O renderer não deve exibir o chip por
inferência em telas cuja política não seja `"alternavel"`.

---

## 23. Rótulos dinâmicos `Todos`/`Executar` e chip `Espaço` da seleção múltipla (ADR-0034)

A ADR-0034 (2026-07-28) fecha a semântica operacional do chip `[␣]` e do
rótulo dinâmico de `[⏎]` para instâncias de `console` com
`politica_selecao: multipla` (`ITEM-0006`). Esta seção propaga essas
decisões; a semântica comportamental completa da seleção pertence a
`contrato_console.md` seção 23.

### 23.1 Chip `Espaço` (D-SEL-05, D-SEL-09)

- existe quando a instância de `console` em foco declara `politica_selecao:
  multipla`;
- ativo quando o item sob cursor é selecionável; inativo quando não é;
- alterna a inclusão do item em foco sem mover o cursor.

### 23.2 Rótulo dinâmico de `[⏎]` — `Todos` e `Executar` (D-SEL-06, D-SEL-07; ADR-0037)

| Estado da seleção | Rótulo | Efeito |
|---|---|---|
| Vazia | `Todos` | Seleciona todos os itens selecionáveis do conjunto filtrado, em todas as páginas; permanece visível e inativo quando não há item selecionável |
| Não vazia | `Executar` | Executa a operação consumidora focal do binding (`contrato_console.md` §23.6 e §23.9) |

Ativação real de `Executar` (ADR-0037 D-H4-05) — ativo somente quando forem
verdadeiras, cumulativamente:

```yaml
- lote_reconciliado_nao_vazio
- executor_focal_disponivel
- tela_resultado_execucao_prevalidada
```

Quando a reconciliação esvaziar o lote no próprio acionamento:

```yaml
executar: false
selecionar_todos_no_mesmo_acionamento: false
selecao_final: vazia
rotulo_final: Todos
```

Este rótulo dinâmico já estava previsto de forma genérica na seção 4.5 de
`docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`; a ADR-0034 fecha sua
condição de disparo e a ADR-0037 fecha a ativação real de `Executar` no
Handoff 4.

### 23.3 Chip específico `[Ins] Dry-Run` (ADR-0037)

```text
[Ins] Dry-Run
```

Semântica:

- sempre visível na tela integrada do Handoff 4;
- ativo nos estados ligado e desligado — nunca usa `cor_inativo`;
- `Insert` alterna execução real e `dry-run`;
- desligado usa a cor normal do preset de chip ativo;
- ligado usa `cor_alerta` (`amarelo`);
- não produz outro eco (mensagem, popup, status ou linha adicional).

Posicionamento: faixa canônica já vigente para chips específicos (entre
`[⏎]` e `[V]`/`[?]`); não cria nova regra de ordenação.

**Supersessão pontual (ADR-0037 D-H4-04)**: esta seção substitui a proibição
anterior de chip de alternância entre execução real e `dry-run` contida em
D-SEL-19 da ADR-0034 e a fronteira correspondente que esta seção registrava
antes da ADR-0037. Todas as demais decisões das ADRs 0034, 0035 e 0036
permanecem vigentes. O toggle é especialização focal do Handoff 4 — não
implementação ou reconciliação do padrão universal (`ITEM-0020` permanece
aberto).

### 23.3.1 Controle universal `[Ins] Real` / `[Ins] Simulação` (ADR-0040)

O controle universal existe somente quando a tela declara validamente, na raiz
do `tela.json`, `controle_execucao` com o campo obrigatório
`controle_execucao.modo_inicial` em `executar` ou `dry_run`, e satisfaz a
compatibilidade integral das ações de processo relevantes com os dois modos.
Na ausência do objeto, com objeto inválido ou sem essa compatibilidade, o chip
universal não existe.

Quando declarado validamente, ele é um chip específico padronizado e
reutilizável. Permanece na faixa dos chips específicos, fora da lista de chips
canônicos, e usa a tecla `Insert` com rótulo dinâmico:

```text
[Ins] Real
[Ins] Simulação
```

Rótulos vigentes fixados por D-DRY-12, que substituem os rótulos `[Ins]
Executar`/`[Ins] Dry-Run` originalmente fixados por D-DRY-02 (histórico
substituído). O chip permanece ativo e operável nos dois estados. Em `Real`,
usa a aparência ativa normal; somente em `Simulação` o texto usa `cor_alerta`.
O rótulo indica o modo em que a futura execução ocorrerá — distinção
obrigatória em relação ao chip de ação `[⏎] Executar`, que inicia o
processamento do lote atual; os dois chips não colidem lexicalmente. O rótulo
é a indicação primária e a cor é reforço visual. Existe um único modo corrente
por instância da tela; ele não é um estado independente do console focado nem
do item corrente. A distinção é obrigatória: este controle universal é o padrão
reutilizável da ADR-0040, não é chip canônico, enquanto o `[Ins] Dry-Run`
acima continua sendo a especialização focal da ADR-0037 para o Handoff 4 do
`ITEM-0006`, com rótulo próprio inalterado por D-DRY-12. Esta seção não migra
nem altera a instância focal.
O rótulo representa o modo corrente; a inicialização, a preservação durante a
mesma instância e a reinicialização em nova abertura ou recarga pertencem ao
ciclo de vida da tela, conforme `contrato_tela_json.md`, e não à barra.

### 23.4 Instância concreta da tela de resultado (ADR-0036)

A ADR-0036 (2026-07-29) fecha a instância concreta da `barra_de_menus` da
tela padrão de resultado `resultado_execucao` (`contrato_tela_json.md` §34.7):

```yaml
barra_de_menus:
  distribuicao: horizontal
  chips:
    - id: esc
      tecla: Esc
      texto: Voltar
      acao: voltar
```

Nenhum outro chip é declarado nessa instância — nem `[⏎]`, `[✥]`, `[⇆]`,
`[␣]` nem `[V]`. A declaração do chip `Esc`/`Voltar` é estruturalmente
válida desde o Handoff 3; a execução funcional do retorno, a suspensão da
tela de origem e a restauração pertencem exclusivamente ao Handoff 4
(ADR-0036 D-H3-19, que substitui pontualmente, quanto a essa tela, a
divisão original de D-SEL-21 da ADR-0034).

### 23.5 Remissões

- `docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md`;
- `docs/adr/ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado.md`;
- `docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md`;
- `docs/contratos/contrato_console.md` — seção 23: seleção múltipla e fluxo focal;
- `docs/contratos/contrato_json_console.md` — seção 14: protocolo provisório e resultado estruturado;
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` — terminologia de chip e rótulo dinâmico.

---

## 24. Paginação interativa limitada — `[<][>]` (ADR-0038)

A ADR-0038 (2026-07-29) fecha a paginação interativa do `console`, deferida
pela ADR-0031 (D15) para o `ITEM-0003`. Esta seção propaga as decisões que
afetam a `barra_de_menus`; a semântica comportamental completa da página
pertence a `contrato_console.md` seção 24.

### 24.1 Topologia limitada

`[<][>]` pertencem à `barra_de_menus`, com existência declarativa
(`paginacao: com`, §8.3) e ativação dinâmica recalculada a cada render. A
topologia entre páginas é limitada, não circular: `[<]` fica inativo na
primeira página; `[>]` fica inativo na última; ambos ficam inativos quando há
apenas uma página (`página 1/1`), inclusive quando o conjunto de itens
visíveis é vazio. Não existe estado visual `página 0/0`.

### 24.2 Alvo dos comandos — console focado

Os controles `[<][>]` avaliam e afetam exclusivamente a página do console
focado. Sem console focado, ou com o console focado sem `paginacao: com`
declarada, ambos ficam inativos. O acionamento de `[<][>]` não altera a
página de nenhum outro console nem o foco corrente — o estado de página é
independente por console (ADR-0038 D-PAG-13), mesmo princípio de
independência já aplicado à seleção múltipla (ADR-0034 D-SEL-01).

### 24.3 Indicador de página não é chip

O indicador `página X/Y` é elemento textual da borda do corpo paginado
(`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` §4.4), não
um chip da `barra_de_menus`. `[<][>]` são os chips que acionam a troca de
página; o indicador é exibido independentemente da existência desses chips.

### 24.4 Entradas aceitas

```yaml
pagina_anterior:
  entradas_aceitas: [",", "<"]
proxima_pagina:
  entradas_aceitas: [".", ">"]
chips_exibidos:
  anterior: "[<]"
  proxima: "[>]"
```

A tradução de tecla física para esses caracteres permanece de implementação.

### 24.5 `[✥]` restrito à página atual

`[✥]` (§11) passa a considerar somente a navegabilidade da página atual do
console focado: aparece quando essa página possui mais de um item navegável;
fica ausente quando a página atual tem zero ou um item navegável, mesmo que
outras páginas do mesmo console possuam mais itens navegáveis (ADR-0038
D-PAG-04). Esta especialização não altera a distinção `[⇆]` × `[✥]` já
fixada na seção 8.3.

### 24.6 Remissões

- `docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md` — decisões D-PAG-01 a D-PAG-14;
- `docs/contratos/contrato_console.md` — seção 24: comportamento completo da paginação;
- `docs/contratos/contrato_chip.md` — regras de existência e ativo/inativo de `[<][>]` e `[✥]`;
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` — indicador de paginação e termos de página;
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` — terminologia de `[<][>]` e `[✥]`.
