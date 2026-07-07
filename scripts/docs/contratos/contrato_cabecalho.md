---
name: contrato-cabecalho
description: Schema e regras do cabecalho — região fixa superior da tela, distinta do corpo, dashboard, lancador e barra_de_menus
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/NOMENCLATURA.md#7-cabecalho"
    reaproveitado_de_legado: false
---

# Contrato — cabecalho

## 1. Objetivo

Especificar o `cabecalho`: sua natureza de região fixa superior da tela, os
dois campos textuais que o compõem, os parâmetros de apresentação de cada
campo, a semântica de renderização, e as regras de uso que vinculam todos os
renderers a este contrato.

Este contrato cobre a seção 7 de `docs/NOMENCLATURA.md`. Estilo universal
(`contrato_estilo.md`, `ativo`), composição de corpo
(`contrato_composicao_corpo.md`, `ativo`) e `barra_de_menus`
(`contrato_barra_de_menus.md`, `ativo`) são módulos separados e externos —
este contrato pode referenciá-los como dependências, mas não redefine nem
duplica suas regras.

---

## 2. Distinção fundamental — `cabecalho` como região própria

O `cabecalho` é uma região distinta de todas as outras regiões da tela.
Nenhum código, documentação ou nomenclatura pode tratar o `cabecalho` como
equivalente a, ou subconjunto de, corpo, `dashboard`, `lancador` ou `barra_de_menus`.

| Conceito | O que é | Localização | Regido por |
|---|---|---|---|
| `cabecalho` | Região fixa superior da tela com título e descrição | Sempre presente, acima do corpo | Este contrato |
| Corpo | Região variável do meio da tela — contém objetos tipo `console`, `lancador` ou `dashboard` | Entre `cabecalho` e `barra_de_menus` | `contrato_composicao_corpo.md` |
| `barra_de_menus` | Região fixa inferior com chips de ação e navegação | Abaixo do corpo | `contrato_barra_de_menus.md` |

**Consequências diretas desta distinção:**

- O `cabecalho` **não herda** nenhuma regra de layout, vão, alinhamento ou
  distribuição do corpo, do objeto `dashboard`, do objeto `lancador` do corpo, nem da
  `barra_de_menus`.
- O arquivo de dados é exclusivo: `config/cabecalho.json` guarda somente
  parâmetros de apresentação do `cabecalho` — não é consultado por nenhum
  outro renderer.
- Os textos concretos de `titulo` e `descricao` pertencem à classe/tela que
  os declara, nunca a `config/cabecalho.json`.

---

## 3. Presença e estrutura

**O `cabecalho` sempre existe.** Não é opcional, condicional, nem pode ser
omitido por uma classe de tela.

O `cabecalho` tem exatamente dois campos textuais:

| Campo | Função | Restrição |
|---|---|---|
| `titulo` | Texto curto de identificação da tela | Sem limite de caracteres definido — o estilo de apresentação é configurável via `config/cabecalho.json` |
| `descricao` | Texto longo de contextualização | Máximo de 200 caracteres (`max_caracteres` em `config/cabecalho.json`) |

Não existem outros campos textuais no `cabecalho`. A classe/tela declara os
valores concretos de `titulo` e `descricao`; este contrato especifica apenas
como esses valores são apresentados.

---

## 4. Fonte dos valores concretos

Todos os parâmetros de apresentação do `cabecalho` — posição do título,
recuo lateral, capitalização, formato na borda, alinhamento da descrição,
limite de caracteres — vivem em **`config/cabecalho.json`**.

Este contrato define a **semântica**, as **regras** e os **invariantes**.
O JSON guarda os **valores concretos de apresentação**. Os dois artefatos têm
responsabilidades separadas e não sobrepostas (política da seção 0 de
`docs/NOMENCLATURA.md`).

O renderer deve ler `config/cabecalho.json` em tempo de execução. Nenhum
parâmetro de apresentação do `cabecalho` pode estar hardcoded no código.

---

## 5. Schema de apresentação — `titulo`

O campo `titulo` é renderizado integrado à linha superior da borda do
`cabecalho`. Os parâmetros abaixo são todos lidos de `config/cabecalho.json`.

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `posicao` | `esquerda` \| `centro` \| `direita` | Posição horizontal do bloco do título na linha da borda superior |
| `recuo_lateral` | inteiro ≥ 0 | Distância em caracteres do canto esquerdo (posicao `esquerda`) ou do canto direito (posicao `direita`). Ignorado quando `posicao = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` | Transformação aplicada ao texto do `titulo` antes da renderização |
| `formato_na_borda` | `com_espacos_laterais` | Estilo de integração do título à linha da borda superior |

**Semântica de `formato_na_borda`:**

- `com_espacos_laterais`: o bloco exibido é `borda + espaço + título + espaço + borda`.

**Semântica de `posicao`:**

- `esquerda`: o bloco do título inicia a `recuo_lateral` caracteres do canto esquerdo da borda.
- `centro`: o bloco do título fica centralizado na linha da borda superior; `recuo_lateral` é ignorado.
- `direita`: o bloco do título termina a `recuo_lateral` caracteres do canto direito da borda.

---

## 6. Schema de apresentação — `descricao`

O campo `descricao` é renderizado abaixo da linha superior da borda, dentro
do espaço do `cabecalho`. Os parâmetros abaixo são todos lidos de
`config/cabecalho.json`.

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `max_caracteres` | inteiro > 0 | Número máximo de caracteres; texto que exceder esse limite é truncado antes da renderização |
| `alinhamento` | `esquerda` \| `centro` \| `direita` | Alinhamento horizontal do texto da descrição |
| `recuo` | inteiro ≥ 0 | Distância em caracteres da borda esquerda (alinhamento `esquerda`) ou da borda direita (alinhamento `direita`). Ignorado quando `alinhamento = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` | Transformação aplicada ao texto da `descricao` antes da renderização |

**Semântica de `alinhamento`:**

- `esquerda`: a descrição começa a `recuo` caracteres da borda esquerda.
- `centro`: a descrição fica centralizada na largura disponível; `recuo` é ignorado.
- `direita`: a descrição termina a `recuo` caracteres da borda direita.

---

## 7. Regras de uso

**R-1. Presença obrigatória.**
O `cabecalho` existe em toda tela do sistema. Nenhuma classe de tela pode
omiti-lo ou declará-lo como condicional.

**R-2. Dois campos, sem extensão.**
O `cabecalho` tem exatamente `titulo` e `descricao`. Nenhum renderer pode
adicionar um terceiro campo ao `cabecalho` sem nova decisão documental e
atualização deste contrato.

**R-3. Textos pertencem à classe.**
Os valores concretos de `titulo` e `descricao` são declarados pela
classe/tela, não lidos de `config/cabecalho.json`. O JSON guarda somente
parâmetros de apresentação.

**R-4. Proibição de hardcoding.**
Nenhum parâmetro de apresentação do `cabecalho` pode estar hardcoded no
código. Todos os parâmetros vêm de `config/cabecalho.json`, lido em tempo
de execução.

**R-5. Independência de layout.**
O renderer do `cabecalho` não consulta, herda nem aplica regras de layout do
corpo (`contrato_composicao_corpo.md`), do objeto `dashboard`, do objeto `lancador`
do corpo, nem da `barra_de_menus` (`contrato_barra_de_menus.md`).

**R-6. `recuo_lateral` ignorado quando `posicao = centro`.**
Quando `titulo.posicao = centro`, o campo `recuo_lateral` é ignorado — o
bloco do título fica centralizado independente do valor numérico de
`recuo_lateral`.

**R-7. `recuo` ignorado quando `alinhamento = centro`.**
Quando `descricao.alinhamento = centro`, o campo `recuo` é ignorado — o
texto da descrição fica centralizado independente do valor numérico de
`recuo`.

**R-8. Truncamento antes da renderização.**
Se o texto de `descricao` exceder `max_caracteres`, ele é truncado antes de
qualquer operação de alinhamento ou capitalização — o alinhamento opera sobre
o texto já truncado.

---

## 8. Critérios de validação

- [ ] O `cabecalho` existe em toda tela do sistema — nenhuma tela é renderizada sem ele.
- [ ] O `cabecalho` contém exatamente os campos `titulo` e `descricao` — nem mais, nem menos.
- [ ] Os valores concretos de `titulo` e `descricao` são declarados pela classe/tela — não constam em `config/cabecalho.json`.
- [ ] Nenhum parâmetro de apresentação do `cabecalho` está hardcoded no código — todos vêm de `config/cabecalho.json`.
- [ ] `titulo` aparece integrado à linha superior da borda no formato `com_espacos_laterais` (borda + espaço + título + espaço + borda).
- [ ] Quando `posicao = esquerda`, o bloco do título inicia a `recuo_lateral` caracteres do canto esquerdo da borda.
- [ ] Quando `posicao = centro`, o bloco do título fica centralizado; `recuo_lateral` é ignorado.
- [ ] Quando `posicao = direita`, o bloco do título termina a `recuo_lateral` caracteres do canto direito da borda.
- [ ] Quando `alinhamento = esquerda`, a descrição começa a `recuo` caracteres da borda esquerda.
- [ ] Quando `alinhamento = centro`, a descrição fica centralizada; `recuo` é ignorado.
- [ ] Quando `alinhamento = direita`, a descrição termina a `recuo` caracteres da borda direita.
- [ ] Texto de `descricao` que exceder `max_caracteres` é truncado antes da renderização.
- [ ] A distinção `cabecalho` vs corpo é verificável: nenhuma regra de `contrato_composicao_corpo.md` é consultada pelo renderer do `cabecalho`.
- [ ] A distinção `cabecalho` vs `barra_de_menus` é verificável: nenhuma regra de `contrato_barra_de_menus.md` é consultada pelo renderer do `cabecalho`.

---

## 9. Pendências em aberto

Nenhuma pendência em aberto para este contrato no momento da emissão.
