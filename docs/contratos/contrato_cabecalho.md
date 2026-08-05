---
name: contrato-cabecalho
description: Schema e regras do cabecalho — região fixa superior da tela, distinta do corpo, dashboard, lancador e barra_de_menus
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao: "docs/nomenclatura/30_CABECALHO.md"
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
    reaproveitado_de_legado: false
  dependencias_nomenclatura:
    dependencias_obrigatorias:
      - docs/nomenclatura/01_NUCLEO_COMUM.md
      - docs/nomenclatura/30_CABECALHO.md
    dependencias_condicionais:
      - modulo: docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
        quando: tratar caminho ou natureza do artefato de configuração do cabeçalho
      - modulo: docs/nomenclatura/10_ESTILO.md
        quando: tratar aparência do cabeçalho
---

# Contrato — cabecalho

## 1. Objetivo

Especificar o `cabecalho`: sua natureza de região fixa superior da tela, os
dois campos textuais que o compõem, os parâmetros de apresentação de cada
campo, a semântica de renderização, e as regras de uso que vinculam todos os
renderers a este contrato.

Este contrato cobre a terminologia de `docs/nomenclatura/30_CABECALHO.md`. Estilo universal
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
- Os textos concretos de `titulo` e `descricao`, assim como os parâmetros locais
  de apresentação do `cabecalho`, pertencem ao objeto `cabecalho` do JSON
  estrutural da respectiva tela.
- O contrato deste módulo define o schema, a semântica, os invariantes e as
  validações; o JSON estrutural da tela guarda os valores concretos da
  instância que declara.

---

## 3. Presença e estrutura

**O `cabecalho` sempre existe.** Não é opcional, condicional, nem pode ser
omitido por uma classe de tela.

O `cabecalho` é um objeto fechado com três campos diretos obrigatórios:
`titulo`, `descricao` e `apresentacao`. Os dois primeiros são strings; o
terceiro é um objeto fechado de parâmetros locais de apresentação.

```yaml
cabecalho:
  titulo: string
  descricao: string
  apresentacao:
    titulo:
      posicao: <valor definido pelo contrato>
      recuo_lateral: <valor definido pelo contrato>
      capitalizacao: <valor definido pelo contrato>
      formato_na_borda: <valor definido pelo contrato>
    descricao:
      max_caracteres: <inteiro entre 1 e 200, inclusive>
      alinhamento: <valor definido pelo contrato>
      recuo: <valor definido pelo contrato>
      capitalizacao: <valor definido pelo contrato>
```

O bloco `apresentacao` e os subobjetos `apresentacao.titulo` e
`apresentacao.descricao` são obrigatórios. Cada subobjeto contém exatamente os
campos listados acima, todos declarados localmente no JSON estrutural da tela.

Os campos textuais são:

| Campo | Função | Restrição |
|---|---|---|
| `titulo` | Texto curto de identificação da tela | Sem limite de caracteres definido — os parâmetros locais de apresentação são declarados no JSON estrutural da tela |
| `descricao` | Texto longo de contextualização | `max_caracteres` é inteiro entre `1` e `200`, inclusive; o limite declarado vale para o texto antes das demais transformações |

Não existem outros campos diretos nem outros campos textuais diretos no
`cabecalho`. A classe/tela declara os valores concretos de `titulo` e
`descricao` e todos os valores de `apresentacao`; este contrato especifica
como esses valores são apresentados.

Pela ADR-0022, a futura tela inicial real `orquestrador` deverá declarar
`cabecalho`, mas os valores concretos obrigatórios de `titulo` e `descricao`
permanecem pendentes de decisão documental suficiente. Este contrato não
autoriza inventar título, descrição, versão, estado de Pipeline ou indicador
dinâmico para preencher `config/telas/orquestrador.json`.

---

## 4. Fonte dos valores concretos

Os textos concretos de `titulo` e `descricao` e todos os parâmetros locais de
apresentação do `cabecalho` — posição do título, recuo lateral, capitalização,
formato na borda, alinhamento da descrição e limite de caracteres — são
declarados no objeto `cabecalho` do JSON estrutural da respectiva tela.

Este contrato define o **schema**, a **semântica**, os **invariantes** e as
**validações**. O JSON estrutural da tela guarda os **valores concretos** da
instância, sem sobrepor a autoridade deste contrato.

O renderer deve obter esses textos e parâmetros do JSON estrutural da tela em
tempo de execução. Nenhum parâmetro local de apresentação do `cabecalho` pode
estar hardcoded no código.

---

## 5. Schema de apresentação — `titulo`

O campo `titulo` é renderizado integrado à linha superior da borda do
`cabecalho`. Os parâmetros abaixo são declarados no objeto `cabecalho` do JSON
estrutural da tela.

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `posicao` | `esquerda` \| `centro` \| `direita` | Posição horizontal do bloco do título na linha da borda superior |
| `recuo_lateral` | inteiro ≥ 0 | Distância em caracteres do canto esquerdo (posicao `esquerda`) ou do canto direito (posicao `direita`). Ignorado quando `posicao = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` | Transformação aplicada ao texto do `titulo` antes da renderização |
| `formato_na_borda` | `com_espacos_laterais` | Estilo de integração do título à linha da borda superior |

**Semântica operacional de `inicio_de_frase`:** quando esse valor de
`capitalizacao` for selecionado, a transformação deve, nesta ordem:

1. percorrer o texto na ordem original dos caracteres;
2. considerar alfabético o primeiro caractere `c` para o qual `c.isalpha()`
   — semântica do método `isalpha()` da linguagem Python — retorne `True`;
   esta é a única fonte de verdade sobre o que conta como caractere
   alfabético, sem exceção;
3. essa determinação é independente de locale: nenhuma configuração de
   idioma, região ou codificação externa altera o resultado de `isalpha()`;
4. não normalizar o texto (por exemplo, para as formas NFC ou NFKC) antes da
   busca;
5. preservar literalmente todos os caracteres anteriores ao caractere
   localizado;
6. substituir exclusivamente esse caractere pelo resultado exato de
   `c.upper()` — semântica do método `upper()` da linguagem Python; esse
   resultado pode conter mais de um caractere Unicode, e o texto resultante
   deve incorporar essa expansão por inteiro, sem truncamento;
7. preservar literalmente todos os caracteres posteriores;
8. não procurar nem transformar nenhum outro caractere alfabético depois
   dessa primeira substituição, inclusive em frases posteriores;
9. não converter o restante do texto para minúsculas;
10. devolver o texto original sem alteração quando nenhum caractere do texto
    satisfizer `isalpha()`;
11. devolver string vazia quando a entrada for string vazia.

Esta operação não depende de ASCII, de tabela manual de caracteres, de
idioma, de codificação externa nem de qualquer biblioteca externa; usa
exclusivamente `str.isalpha()` e `str.upper()` da linguagem Python, aplicados
sem normalização prévia e sem consulta a locale. Essa determinação é a única
autoridade sobre o significado de "caractere alfabético" neste contrato — não
há formulação alternativa, dependente de ASCII ou de locale, em vigor. Os
exemplos normativos são:

| Entrada | Resultado | Observação |
|---|---|---|
| `execução da API REST` | `Execução da API REST` | primeiro caractere alfabético é `e` |
| `  execução concluída` | `  Execução concluída` | espaços iniciais preservados |
| `já está OK. segunda frase.` | `Já está OK. segunda frase.` | frases posteriores não são tocadas |
| `123 - execução` | `123 - Execução` | dígitos e sinal inicial preservados |
| `área útil` | `Área útil` | letra acentuada satisfaz `isalpha()` |
| `çalışma` | `Çalışma` | letra com cedilha satisfaz `isalpha()`; resultado independe de locale |
| `Δ resultado` | `Δ resultado` | letra grega já maiúscula; `upper()` não altera o caractere |
| `ßeta` | `SSeta` | `"ß".upper()` produz dois caracteres (`SS`); a expansão é incorporada por inteiro |
| `123 --` | `123 --` | nenhum caractere do texto satisfaz `isalpha()` |
| `""` | `""` | string vazia devolvida sem alteração |

O exemplo `ßeta` → `SSeta` foi obtido por execução direta de
`"ß".upper()` no interpretador Python instalado no ambiente (versão 3.14);
não é um caso hipotético nem uma regra específica desse caractere — é a
evidência de que a regra geral do passo 6 (incorporar por inteiro o
resultado de `upper()`) é necessária.

**Semântica de `formato_na_borda`:**

- `com_espacos_laterais`: o bloco exibido é `borda + espaço + título + espaço + borda`.

**Semântica de `posicao`:**

- `esquerda`: o bloco do título inicia a `recuo_lateral` caracteres do canto esquerdo da borda.
- `centro`: o bloco do título fica centralizado na linha da borda superior; `recuo_lateral` é ignorado.
- `direita`: o bloco do título termina a `recuo_lateral` caracteres do canto direito da borda.

---

## 6. Schema de apresentação — `descricao`

O campo `descricao` é renderizado abaixo da linha superior da borda, dentro
do espaço do `cabecalho`. Os parâmetros abaixo são declarados no objeto
`cabecalho` do JSON estrutural da tela.

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `max_caracteres` | inteiro entre `1` e `200`, inclusive | Número máximo de caracteres; texto que exceder esse limite é truncado antes das demais transformações |
| `alinhamento` | `esquerda` \| `centro` \| `direita` | Alinhamento horizontal do texto da descrição |
| `recuo` | inteiro ≥ 0 | Distância em caracteres da borda esquerda (alinhamento `esquerda`) ou da borda direita (alinhamento `direita`). Ignorado quando `alinhamento = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` \| `preservar` | Transformação aplicada ao texto da `descricao` antes da renderização |

`max_caracteres` é obrigatório, aceita somente valor inteiro entre `1` e
`200`, inclusive, e não possui default.

Exemplos de domínio: `1` e `200` são válidos; `0`, números negativos,
`201` e valores não inteiros são inválidos.

### Semântica da capitalização da descrição

Depois do corte contratual por `max_caracteres`, aplica-se exatamente um dos
valores declarados no campo `capitalizacao`:

- `maiusculas`: converter integralmente o texto cortado com `str.upper()`.
- `inicio_de_frase`: localizar o primeiro caractere cujo `isalpha()` seja
  verdadeiro e substituí-lo pelo resultado integral de `upper()`, preservando
  todos os demais caracteres; a operação é independente de locale, não faz
  normalização Unicode e permite a expansão Unicode de `upper()`.
- `preservar`: manter exatamente o texto cortado. Nenhum caractere é
  convertido, removido, inserido, normalizado ou reinterpretado pela etapa de
  capitalização; não procurar caractere alfabético, não aplicar `upper()` ou
  `lower()`, não consultar locale, não alterar prefixo, sufixo ou frases
  posteriores e não criar alias. `preservar` é um valor declarado, não a
  ausência do campo, valor implícito, default ou fallback.

`preservar` é uma operação identidade sobre o texto depois do corte:

```text
"desc fab" → "desc fab"
"Desc fab" → "Desc fab"
"  execução da API REST" → "  execução da API REST"
"123 - execução" → "123 - execução"
"ßeta" → "ßeta"
"" → ""
```

O contraste entre as três escolhas é normativo:

```text
entrada: "desc fab"

preservar:
  resultado: "desc fab"

inicio_de_frase:
  resultado: "Desc fab"

maiusculas:
  resultado: "DESC FAB"
```

Para `inicio_de_frase`, `isalpha()` e `upper()` são os métodos da linguagem
Python; nenhum locale ou normalização é consultado, o primeiro caractere
alfabético é o único transformado, e a expansão Unicode de `upper()` é
incorporada integralmente. Prefixo, sufixo e frases posteriores permanecem
literais.

### Ordem de transformação da descrição

A descrição deve ser processada nesta ordem, sem inversão:

1. cortar o texto pelo limite contratual de `descricao.max_caracteres`;
2. aplicar a capitalização selecionada, entre `maiusculas`, `inicio_de_frase`
   e `preservar`;
3. aplicar alinhamento e recuo;
4. sujeitar o resultado à limitação geométrica já contratada.

O último passo não cria nem altera uma política de overflow: aplica somente a
limitação geométrica já prevista neste contrato.

**Semântica de `alinhamento`:**

- `esquerda`: a descrição começa a `recuo` caracteres da borda esquerda.
- `centro`: a descrição fica centralizada na largura disponível; `recuo` é ignorado.
- `direita`: a descrição termina a `recuo` caracteres da borda direita.

### Consequência normativa para a migração

`preservar` existe para representar apresentação local sem transformação de
caixa. A escolha concreta do valor pertence à tela. Migrações que pretendem
preservar descrições anteriormente renderizadas literalmente devem declarar
`preservar`; `inicio_de_frase` continua disponível como escolha explícita para
telas que desejem essa transformação. A ausência de
`apresentacao.descricao.capitalizacao` é inválida.

---

## 7. Regras de uso

**R-1. Presença obrigatória.**
O `cabecalho` existe em toda tela do sistema. Nenhuma classe de tela pode
omiti-lo ou declará-lo como condicional.

**R-2. Estrutura fechada e campos obrigatórios.**
O `cabecalho` é um objeto fechado com exatamente os campos diretos obrigatórios
`titulo`, `descricao` e `apresentacao`. `titulo` e `descricao` são strings;
`apresentacao` é objeto obrigatório e fechado, com exatamente os subobjetos
obrigatórios `apresentacao.titulo` e `apresentacao.descricao`. O primeiro tem
exatamente `posicao`, `recuo_lateral`, `capitalizacao` e `formato_na_borda`; o
segundo tem exatamente `max_caracteres`, `alinhamento`, `recuo` e
`capitalizacao`. Parâmetros desconhecidos, aliases, schema alternativo,
fallback e segundo local de configuração são inválidos.

**R-3. Textos pertencem à classe.**
Os valores concretos de `titulo` e `descricao` são declarados pela
classe/tela, no JSON estrutural da respectiva tela. Os parâmetros locais de
apresentação também são declarados nesse JSON; nenhum deles é fornecido por
um arquivo global separado.

**R-4. Proibição de hardcoding.**
Nenhum parâmetro de apresentação do `cabecalho` pode estar hardcoded no
código. Todos os textos e parâmetros locais vêm do JSON estrutural da tela,
lido em tempo de execução, sem valores implícitos ou fallback.

**R-5. Fronteira com estilo global.**
Os parâmetros locais de apresentação do `cabecalho` não pertencem a
`config/estilo.json`. Esse arquivo fornece somente aparência global
compartilhada, conforme o contrato de estilo.

**R-6. Independência de layout.**
O renderer do `cabecalho` não consulta, herda nem aplica regras de layout do
corpo (`contrato_composicao_corpo.md`), do objeto `dashboard`, do objeto `lancador`
do corpo, nem da `barra_de_menus` (`contrato_barra_de_menus.md`).

**R-7. `recuo_lateral` ignorado quando `posicao = centro`.**
Quando `titulo.posicao = centro`, o campo `recuo_lateral` é ignorado — o
bloco do título fica centralizado independente do valor numérico de
`recuo_lateral`.

**R-8. `recuo` ignorado quando `alinhamento = centro`.**
Quando `descricao.alinhamento = centro`, o campo `recuo` é ignorado — o
texto da descrição fica centralizado independente do valor numérico de
`recuo`.

**R-9. Truncamento antes da renderização.**
Se o texto de `descricao` exceder `max_caracteres`, ele é truncado primeiro;
depois são aplicadas a capitalização e, em seguida, o alinhamento e o recuo;
por último, o resultado é submetido à limitação geométrica já contratada.

---

## 8. Critérios de validação

- [ ] O `cabecalho` existe em toda tela do sistema — nenhuma tela é renderizada sem ele.
- [ ] O `cabecalho` é objeto fechado com os três campos diretos obrigatórios `titulo`, `descricao` e `apresentacao`.
- [ ] `titulo` e `descricao` são strings; `apresentacao` é objeto fechado com os subobjetos obrigatórios `apresentacao.titulo` e `apresentacao.descricao`.
- [ ] `apresentacao.titulo` contém exatamente `posicao`, `recuo_lateral`, `capitalizacao` e `formato_na_borda`.
- [ ] `apresentacao.descricao` contém exatamente `max_caracteres`, `alinhamento`, `recuo` e `capitalizacao`.
- [ ] Os valores concretos de `titulo`, `descricao` e dos parâmetros locais são declarados no JSON estrutural da respectiva tela.
- [ ] Nenhum parâmetro local de apresentação do `cabecalho` está hardcoded no código, recebe valor implícito/fallback ou é lido de `config/estilo.json` ou de outro local global.
- [ ] Parâmetros desconhecidos e aliases são rejeitados.
- [ ] `titulo` aparece integrado à linha superior da borda no formato `com_espacos_laterais` (borda + espaço + título + espaço + borda).
- [ ] Quando `posicao = esquerda`, o bloco do título inicia a `recuo_lateral` caracteres do canto esquerdo da borda.
- [ ] Quando `posicao = centro`, o bloco do título fica centralizado; `recuo_lateral` é ignorado.
- [ ] Quando `posicao = direita`, o bloco do título termina a `recuo_lateral` caracteres do canto direito da borda.
- [ ] Quando `alinhamento = esquerda`, a descrição começa a `recuo` caracteres da borda esquerda.
- [ ] Quando `alinhamento = centro`, a descrição fica centralizada; `recuo` é ignorado.
- [ ] Quando `alinhamento = direita`, a descrição termina a `recuo` caracteres da borda direita.
- [ ] `max_caracteres` é obrigatório, não possui default e aceita somente inteiro entre `1` e `200`, inclusive.
- [ ] Valores `0`, negativos, superiores a `200` e não inteiros de `max_caracteres` são rejeitados.
- [ ] `inicio_de_frase` altera somente o primeiro caractere alfabético, preserva literalmente os demais caracteres, não converte o restante para minúsculas e não transforma frases posteriores.
- [ ] `preservar` mantém exatamente o texto após o corte por `max_caracteres`, sem conversão, remoção, inserção, normalização ou reinterpretação.
- [ ] A ordem da descrição é corte por `max_caracteres`, capitalização, alinhamento e recuo, e limitação geométrica já contratada.
- [ ] A distinção `cabecalho` vs corpo é verificável: nenhuma regra de `contrato_composicao_corpo.md` é consultada pelo renderer do `cabecalho`.
- [ ] A distinção `cabecalho` vs `barra_de_menus` é verificável: nenhuma regra de `contrato_barra_de_menus.md` é consultada pelo renderer do `cabecalho`.

---

## 9. Critérios de erro

O carregamento ou a validação da tela deve falhar quando:

- `cabecalho` não existir, não for objeto ou não contiver exatamente os três campos diretos obrigatórios;
- `titulo` ou `descricao` não forem strings;
- `apresentacao`, `apresentacao.titulo` ou `apresentacao.descricao` não existirem, não forem objetos ou não contiverem exatamente os campos obrigatórios;
- qualquer enumeração, tipo ou limite das seções 5 e 6 for violado;
- `max_caracteres` for zero, negativo, superior a `200` ou não for inteiro;
- houver parâmetro desconhecido, alias, schema alternativo, valor implícito, fallback ou tentativa de leitura de configuração global/segundo local.

## 10. Pendências em aberto

Nenhuma pendência em aberto para este contrato no momento da emissão.
