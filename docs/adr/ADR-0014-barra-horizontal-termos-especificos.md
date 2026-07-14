---
name: ADR-0014-barra-horizontal-termos-especificos
description: barra_de_menus.distribuicao = horizontal como distribuicao horizontal RESPONSIVA dos chips (alias transitório de modo = horizontal_responsiva); estrutura canônica futura como objeto declarativo; regra contra alteração normativa por filtro parcial de substring; não implementa renderização nem altera JSON/testes
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
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_processo_desenvolvimento.md
  handoffs_bloqueados: []
---

# ADR-0014 — Distribuição horizontal responsiva da `barra_de_menus` e termos específicos

## Status

`aceita`

## Data

2026-07-09

## Contexto

A ADR-0011 fixou a terminologia final de `corpo.arranjo` em `vertical`/
`horizontal`. A ADR-0012 fixou que a `barra_de_menus` é declarativa por tela.
Restaram três pendências normativas relacionadas, todas decorrentes do mesmo
levantamento técnico/documental em modo somente leitura:

1. **Distribuição visual da `barra_de_menus`** — os JSONs ativos
   (`orquestrador.json`, `destino_minimo.json`, `grupo_minimo.json`,
   `stub_b.json`) declaram `barra_de_menus.distribuicao = "horizontal"`, mas
   o renderer atual (`tela/renderizador.py`, função `_linhas_barra`) ignora
   essa distribuição e empilha os chips, criando uma linha por chip. Não há
   norma que fixe que `barra_de_menus.distribuicao = "horizontal"` deve ser
   respeitada pelo renderer. A ADR-0012 fixou que a barra é declarativa por
   tela, mas não normatizou a distribuição visual horizontal.

2. **Risco de interpretação simplificada** — uma norma que apenas diga
   "barra horizontal" sem qualificar como os chips se distribuem deixa
   aberta a leitura de "todos os chips forçados em uma única linha fixa".
   Esse vazio normativo permitiria uma implementação que, ao respeitar
   `distribuicao = "horizontal"`, truncasse/omitisse chips ou empilhasse
   verticalmente como fallback genérico sempre que os chips não coubessem
   em uma linha. É preciso normatizar `distribuicao = "horizontal"` como
   **distribuição horizontal responsiva**, não como linha única fixa.

3. **Risco terminológico de filtro parcial** — os termos `vertical` e
   `horizontal` circulam no sistema com pelo menos três significados
   distintos: `corpo.arranjo` (ADR-0011), `barra_de_menus.distribuicao`
   (ativo) e, futuramente, `ocupacao_vertical_terminal` (ADR-0013). Sem uma
   regra explícita, uma migração futura poderia aplicar uma decisão
   procurando apenas por substrings como `vertical`, `horizontal`, `barra`,
   `chip` ou `arranjo`, atingindo campos/conceitos errados.

A decisão gerencial é normatizar as três questões em uma única ADR com duas
partes: a **Parte A** normatiza `barra_de_menus.distribuicao = "horizontal"`
como distribuição horizontal responsiva (e registra a estrutura canônica
futura como objeto declarativo); a **Parte B** estabelece a regra processual
de alteração por termo específico completo, que protege a Parte A (e a
ADR-0013, e a ADR-0011) de alterações por filtro parcial.

Esta ADR é normativa. Ela **não** implementa a renderização horizontal da
barra, **não** altera `tela/`, **não** altera testes e **não** altera JSONs
de produção — essas são pendências de handoff futuro. Em particular, ela
**não** migra nenhum JSON do formato string `"horizontal"` para o formato
canônico futuro (objeto declarativo); esse formato é registrado aqui como
**meta futura**, aplicável em handoff posterior.

---

## Decisão

A decisão é composta de duas partes: a **Parte A** normatiza
`barra_de_menus.distribuicao = "horizontal"` como **distribuição horizontal
responsiva** e registra a estrutura canônica futura; a **Parte B** estabelece
a regra processual de alteração por termo específico completo.

### Parte A — `barra_de_menus.distribuicao = "horizontal"` é distribuição horizontal responsiva

**A.1. A `barra_de_menus` continua declarativa por tela, conforme ADR-0012.**

A política declarativa por tela (ADR-0012) é preservada integralmente. Esta
Parte A apenas normatiza a distribuição visual, não reabre a política
declarativa.

**A.2. A distribuição visual da barra é controlada por termo específico:
`barra_de_menus.distribuicao`.**

O campo que controla a distribuição visual da barra é
`barra_de_menus.distribuicao`, termo específico completo. Não é
`corpo.arranjo`, não é `tiling`, não é `posicao_dashboard`.

**A.3. `barra_de_menus.distribuicao = "horizontal"` NÃO significa linha
única fixa.**

O valor string `"horizontal"` **não** obriga todos os chips a uma única linha
fixa e inquebrável. Reduzir `distribuicao = "horizontal"` a "linha única
simples" é uma interpretação proibida por esta ADR, porque abriria caminho
para truncar texto, omitir chips ou empilhar verticalmente como fallback
genérico sempre que os chips não couberem em uma linha.

**A.4. `barra_de_menus.distribuicao = "horizontal"` SIGNIFICA distribuição
horizontal responsiva dos chips da barra.**

`barra_de_menus.distribuicao = "horizontal"` significa **distribuição
horizontal responsiva**: o renderer tenta dispor os chips lado a lado na
linha/região da barra; se não couberem em uma única linha dentro dos limites
declarados, a barra quebra em multilinha de forma determinística conforme os
parâmetros declarados — nunca empilhando um chip por linha como fallback
genérico.

**A.5. A string `"horizontal"` é formato transitório.**

O valor string `"horizontal"` (ativo nos JSONs de produção) é aceito
transitoriamente como **alias** de
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"`, com defaults
definidos pelo contrato ou pelo handoff aplicável. O formato string **não**
é o formato canônico final.

**A.6. O formato canônico futuro é objeto declarativo:
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"`.**

O formato canônico futuro de `barra_de_menus.distribuicao` é **objeto
declarativo**, cuja forma base está registrada na seção "Estrutura canônica
futura" abaixo. A migração de JSON/código/testes para esse formato ocorre em
handoff futuro, **não** nesta ADR.

**A.7. O renderer deve respeitar a distribuição declarada na instância.**

A distribuição declarada na instância da `barra_de_menus` é a fonte de
decisão visual para a disposição dos chips. O renderer aplica a declaração;
não decide distribuição por conta própria nem por largura de terminal.

**A.8. O renderer não deve empilhar um chip por linha quando a distribuição
declarada for horizontal/horizontal_responsiva.**

O comportamento atual de `_linhas_barra` (um chip por linha) é incompatível
com `barra_de_menus.distribuicao = "horizontal"` e deve ser corrigido em
handoff futuro. Enquanto a distribuição não for implementada, o renderer
permanece como está; esta ADR não força a implementação agora.

**A.9. O renderer não deve reordenar chips por heurística própria.**

A ordem de exibição é a declarada em `barra_de_menus.chips[]`, salvo política
explícita de agrupamento/âncoras declarada na própria instância (ver seção
"Ordem e âncoras").

**A.10. O renderer não deve inventar chips ausentes.**

Chips não declarados na instância não ocupam espaço. O renderer não cria
chips por capacidade percebida, por largura de terminal nem por herança.

**A.11. O renderer não deve completar a barra com a lista canônica global.**

A barra não recebe chips canônicos globais por padrão (reforça ADR-0012). A
ausência de um chip canônico é legítima e não deve ser "corrigida" pelo
renderer.

**A.12. O renderer não deve transformar erro de layout em omissão
silenciosa de chip.**

Quando nenhum arranjo declarado couber (overflow), o resultado é **erro
determinístico de layout**, nunca a omissão silenciosa de chips para "fazer
caber" (ver seção "Overflow").

**A.13. A `barra_de_menus` não herda regra do `lancador`.**

A `barra_de_menus` e o `lancador` são entidades distintas (ver
`contrato_barra_de_menus.md` seção 3). Nenhuma regra de layout do
`lancador` (fila/matriz, algoritmo de colunas, vãos do `lancador`) é
herdada pela barra por padrão. Os parâmetros da distribuição responsiva
da barra são declarados na própria instância da barra.

**A.14. Chips de itens do `lancador` não são chips da `barra_de_menus`.**

Chips declarados em itens de `lancador` (ex.: `g`, `d`) não pertencem à
`barra_de_menus`. A distribuição horizontal responsiva normatizada aqui
aplica-se apenas aos chips declarados em `barra_de_menus.chips[]`, não aos
chips dos itens do corpo. Esta regra reforça a distinção já fixada por
`contrato_barra_de_menus.md` seção 3.

**A.15. A distribuição da `barra_de_menus` é independente de
`corpo.arranjo = "horizontal"`.**

`barra_de_menus.distribuicao = "horizontal"` refere-se à disposição dos
chips na região fixa inferior da tela. `corpo.arranjo = "horizontal"`
refere-se à ordem/composição dos elementos do corpo (ADR-0011). São campos
em regiões distintas com semântica própria; um não implica nem proíbe o
outro. Uma tela pode ter `corpo.arranjo = "vertical"` e
`barra_de_menus.distribuicao = "horizontal"` simultaneamente.

**A.16. Esta ADR não implementa a renderização horizontal responsiva da
barra agora.**

Esta ADR não altera `config/`, `tela/`, nem testes. A implementação da
distribuição horizontal responsiva da barra, a migração de JSONs para o
formato canônico futuro e os testes correspondentes são pendências de
handoff futuro.

---

## Estrutura canônica futura de `barra_de_menus.distribuicao`

A ADR registra, como **meta futura**, que a estrutura canônica final de
`barra_de_menus.distribuicao` é objeto declarativo. A forma base de
referência é a abaixo. A migração de JSON/código/testes para esse formato
ocorre em handoff futuro; **esta ADR não cria nem altera nenhum JSON**.

```json
{
  "barra_de_menus": {
    "distribuicao": {
      "modo": "horizontal_responsiva",

      "ordem": {
        "politica": "declaracao",
        "ancoras": {
          "primeiro": ["chip_esc"],
          "ultimo": ["chip_ajuda"]
        }
      },

      "tentativa_inicial": "linha_unica",
      "quebra": "multilinha_quando_nao_couber",
      "preenchimento_multilinha": "coluna_a_coluna",

      "linhas": {
        "minimo": 1,
        "maximo": 2,
        "preferir_menor_numero": true
      },

      "alinhamento_linhas": "esquerda",

      "espacamentos": {
        "margem_horizontal": {
          "minimo": 1,
          "maximo": null
        },
        "vao_chip_texto": {
          "minimo": 1,
          "maximo": 3
        },
        "vao_entre_chips": {
          "minimo": 2,
          "maximo": 6
        },
        "vao_entre_colunas": {
          "minimo": 2,
          "maximo": 8
        },
        "vao_vertical_entre_linhas": {
          "minimo": 0,
          "maximo": 0
        }
      },

      "colunas": {
        "largura": "por_maior_item_da_coluna",
        "subcolunas": {
          "chip": {
            "alinhamento": "esquerda"
          },
          "texto": {
            "alinhamento": "esquerda"
          }
        }
      },

      "overflow": {
        "quando_nao_couber": "erro_layout",
        "nao_omitir_chips": true,
        "nao_truncar_texto": true,
        "nao_reordenar": true
      }
    },

    "chips": []
  }
}
```

---

## Campos e semânticas

Resumo normativo dos campos e dos valores iniciais de
`barra_de_menus.distribuicao`:

- **`modo`**: `horizontal_responsiva`.
- **`tentativa_inicial`**: `linha_unica`.
- **`quebra`**: `multilinha_quando_nao_couber`.
- **`preenchimento_multilinha`**: `coluna_a_coluna` | `linha_a_linha`.
- **`ordem.politica`**: `declaracao` | `grupos_declarados`.
- **`linhas`**: `minimo`, `maximo`, `preferir_menor_numero`.
- **`alinhamento_linhas`**: `esquerda` | `centro` | `direita` | `justificado`.
- **`espacamentos`**: `margem_horizontal`, `vao_chip_texto`,
  `vao_entre_chips`, `vao_entre_colunas`, `vao_vertical_entre_linhas`.
- **`colunas`**: `largura = por_maior_item_da_coluna`;
  `subcolunas.chip.alinhamento = esquerda`;
  `subcolunas.texto.alinhamento = esquerda`.
- **`overflow`**: `quando_nao_couber = erro_layout`;
  `nao_omitir_chips = true`; `nao_truncar_texto = true`;
  `nao_reordenar = true`.

Os valores concretos (mínimos/máximos de vãos, limites de linhas, etc.) são
defaults de referência registrados por esta ADR; o handoff futuro de
implementação pode confirmá-los ou refiná-los no contrato e no JSON, sem
contradizer as semânticas acima.

---

## Algoritmo normativo mínimo

O renderer da barra, ao aplicar `modo = "horizontal_responsiva"`, deve
seguir, no mínimo, este algoritmo:

```text
1. Ler `barra_de_menus.chips[]` da instância da tela.
2. Determinar sequência base:
   - `ordem.politica = "declaracao"` usa a ordem de `barra_de_menus.chips[]`;
   - `ordem.politica = "grupos_declarados"` usa a ordem dos grupos e dos
     chips dentro de cada grupo.
3. Validar âncoras, se declaradas.
4. Calcular largura de cada item:
   `largura_item = largura_chip + vao_chip_texto + largura_texto`.
5. Tentar linha única com margens e vãos mínimos.
6. Se couber, renderizar em uma linha e aplicar alinhamento.
7. Se não couber, tentar multilinha até `linhas.maximo`.
8. Em multilinha, usar `preenchimento_multilinha` declarado:
   - `coluna_a_coluna`; ou
   - `linha_a_linha`.
9. Calcular colunas e subcolunas conforme declaração.
10. Se nenhum arranjo couber, retornar erro determinístico de layout.
```

Este algoritmo é normativo mínimo: impede a leitura simplificada de
"horizontal = linha única simples". O handoff futuro pode detalhar
passos intermediários, mas não pode contradizê-lo.

---

## Ordem e âncoras

A ordem base da `barra_de_menus` é a ordem declarada em
`barra_de_menus.chips[]`.

- A política `ordem.politica = "declaracao"` usa exatamente essa ordem.
- A política `ordem.politica = "grupos_declarados"` usa a ordem dos grupos e
  a ordem dos chips dentro de cada grupo.

Âncoras como `chip_esc` primeiro e `chip_ajuda` último são **restrições de
validação**, não instruções de reordenação automática. Se a ordem declarada
violar uma âncora, a validação falha — o renderer **não** corrige
reordenando.

---

## Overflow

Quando nenhum arranjo declarado couber dentro de `linhas.maximo` (mesmo
após tentar multilinha e os vãos no mínimo), o resultado é
`quando_nao_couber = "erro_layout"`: um **erro determinístico de layout**.

É proibido, para "fazer caber":

- omitir chips (`nao_omitir_chips = true`);
- truncar texto (`nao_truncar_texto = true`);
- reordenar chips (`nao_reordenar = true`).

Erro de layout é erro, não omissão silenciosa.

---

## Proibições

Esta Parte A proíbe explicitamente, no renderer e em qualquer migração
futura:

- hardcodar lista de chips;
- restaurar lista canônica global;
- reordenar chips automaticamente;
- aplicar regra do `lancador` por herança;
- reduzir `horizontal_responsiva` a linha única simples;
- empilhar verticalmente como fallback genérico;
- omitir chip quando não couber;
- truncar texto automaticamente;
- alterar ações ou semântica dos chips;
- implementar layout por heurística não declarada.

---

## Compatibilidade transitória com distribuicao = "horizontal"

O valor string `"horizontal"` permanece aceito transitoriamente e deve ser
interpretado como alias de:

```text
barra_de_menus.distribuicao.modo = "horizontal_responsiva"
```

com defaults definidos pelo contrato ou pelo handoff aplicável.

O formato string não é o formato canônico final. O formato canônico final é
objeto declarativo. Enquanto a migração para o formato canônico não ocorrer,
os JSONs ativos permanecem com `"distribuicao": "horizontal"` — esta ADR
**não** altera esses JSONs.

---

### Parte B — Regra de alteração por termo específico completo

**B.1. Filtros parciais podem ser usados para busca, auditoria e localização.**

Substrings como `vertical`, `horizontal`, `barra`, `chip`, `arranjo` podem
ser usadas em `rg`/`grep`/levantamentos para localizar candidatos a
alteração. O uso para **busca** é permitido.

**B.2. Filtros parciais NÃO podem ser usados como critério de alteração
normativa automática.**

O resultado de uma busca por substring nunca autoriza uma substituição
normativa automatizada. Busca é busca; alteração é alteração. São etapas
distintas.

**B.3. ADRs, contratos, JSONs, código e testes só podem ser alterados quando
o termo específico completo afetado for identificado.**

Antes de aplicar qualquer alteração, deve-se identificar o termo específico
completo que está sendo alterado (ex.: `corpo.arranjo = "vertical"`,
`barra_de_menus.distribuicao = "horizontal"`,
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"`,
`ocupacao_vertical_terminal`). Sem essa identificação, a alteração é
bloqueada.

**B.4. É proibido aplicar uma decisão procurando apenas substrings ambíguas
como:**

- `vertical`;
- `horizontal`;
- `barra`;
- `chip`;
- `arranjo`.

Essas substrings aparecem em múltiplos campos/conceitos com significados
distintos. Usá-las como critério único de alteração é proibido.

**B.5. Toda ADR deve indicar o termo específico completo que está alterando.**

Cada ADR deve, em seu texto, nomear explicitamente o termo específico
completo afetado (campo + valor, ou conceito nomeado). ADRs que afetem
`corpo.arranjo`, `barra_de_menus.distribuicao`, `ocupacao_vertical_terminal`,
etc., devem nomear esses termos, não se referir a eles apenas por substring.

**B.6. Exemplos de termos específicos completos:**

- `corpo.arranjo = "vertical"`;
- `corpo.arranjo = "horizontal"`;
- `barra_de_menus.distribuicao = "horizontal"`;
- `barra_de_menus.distribuicao.modo = "horizontal_responsiva"`;
- `ocupacao_vertical_terminal`;
- `preenchimento_altura_corpo`;
- `chip canônico`;
- `chip declarado por tela`.

A lista acima é exemplificativa, não exaustiva. Outros termos específicos
completos podem existir; o princípio é o mesmo: nomear o campo/conceito por
extenso, não por substring.

**B.7. A busca por termo parcial pode aparecer em levantamento/auditoria,
mas a aplicação da alteração deve ser revisada termo a termo.**

Levantamentos e relatórios de auditoria podem listar candidatos por
substring, desde que cada candidato seja confirmado como termo específico
completo antes da alteração.

**B.8. Esta regra vale para ADRs futuras, handoffs, implementações, migrações
e QAs.**

A regra é processual e transcende artefato: aplica-se a quem escreve ADR,
quem escreve handoff, quem implementa, quem migra JSON/código e quem audita.

---

## Consequências

### Obrigatórias

- **Futuras migrações não devem substituir `vertical` ou `horizontal` de
  forma global.** Migrações devem identificar o termo específico completo
  (`corpo.arranjo`, `barra_de_menus.distribuicao`,
  `barra_de_menus.distribuicao.modo`, `ocupacao_vertical_terminal`, etc.) e
  atuar apenas sobre ele.
- **`barra_de_menus.distribuicao = "horizontal"` deve ser interpretado como
  distribuição horizontal responsiva**, nunca como linha única simples ou
  empilhamento vertical.
- **Contratos devem preferir termos específicos completos.** Contratos
  ativos devem referir-se a campos/conceitos pelo termo completo, evitando
  ambiguidade de substring.
- **Handoffs devem listar explicitamente quais campos/conceitos serão
  alterados.** Handoff que altere distribuição, arranjo ou ocupação deve
  nomear o campo/conceito por extenso em seu escopo.
- **Auditorias devem bloquear alterações por filtro parcial quando houver
  ambiguidade.** QA que detecte substituição por substring ambígua sem
  identificação do termo específico completo deve registrar como achado
  bloqueante.

### Artefatos a atualizar nesta tarefa documental

| Arquivo | Atualização mínima |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0014 com título de distribuição horizontal responsiva |
| `docs/NOMENCLATURA.md` | Diferenciar `barra_de_menus.distribuicao = "horizontal"` (alias transitório de responsiva), `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` (canônico futuro) e `corpo.arranjo = "horizontal"`; registrar que alterações normativas devem usar termos específicos completos |
| `docs/contratos/contrato_tela_json.md` | Registrar `barra_de_menus.distribuicao` como string transitória ou objeto canônico futuro (`modo = "horizontal_responsiva"`); renderer deve respeitar a distribuição declarada conforme ADR-0014 |
| `docs/contratos/contrato_barra_de_menus.md` | Registrar a regra normativa completa: alias transitório; objeto canônico futuro; tentativa de linha única; quebra multilinha; preenchimento declarado; vãos; ordem por declaração; âncoras como validação; overflow determinístico; proibição de empilhar um chip por linha e de omitir/truncar/reordenar |
| `docs/contratos/contrato_processo_desenvolvimento.md` | Manter a regra: filtros parciais para busca; alterações normativas e implementações atingem apenas termos específicos completos; ADRs/handoffs devem declarar o campo/conceito afetado; auditorias bloqueiam substituição por substring ambígua |

### Arquivos que NÃO devem ser alterados por esta ADR

| Arquivo ou grupo | Motivo |
|---|---|
| `config/` | JSONs de produção permanecem; a distribuição já está declarada como string transitória, falta o renderer respeitá-la como responsiva |
| `tela/` | Implementação da distribuição horizontal responsiva no renderer é pendência de handoff futuro |
| `docs/handoff/` | Artefatos históricos permanecem; handoff novo será criado no tempo próprio |
| `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md` | ADR aceita não é reescrita; sua disambiguação `corpo.arranjo` × `barra_de_menus.distribuicao` é preservada e ampliada por esta ADR |
| `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` | ADR aceita não é reescrita; a Parte A complementa (não contradiz) a política declarativa por tela |

### Pendências derivadas

- Handoff futuro de implementação da distribuição horizontal responsiva da
  `barra_de_menus`: fazer o renderer respeitar
  `barra_de_menus.distribuicao = "horizontal"` (alias) /
  `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` (canônico) em
  vez de empilhar um chip por linha, seguindo o algoritmo normativo mínimo
  desta ADR.
- Migração futura dos JSONs ativos do formato string `"horizontal"` para o
  formato canônico objeto declarativo — **não** executada nesta ADR.
- Casos de teste de renderização horizontal responsiva da barra (linha
  única quando couber; multilinha determinística quando não couber; erro de
  layout determinístico quando nenhum arranjo couber).

---

## Fora do escopo desta ADR

Os pontos abaixo não são decididos por esta ADR:

- **Implementar a renderização horizontal responsiva da barra** — pendência
  de handoff futuro.
- **Migrar JSONs para o formato canônico objeto declarativo** — pendência de
  handoff futuro; os JSONs ativos permanecem com `"distribuicao":
  "horizontal"`.
- **Fechar valores finais de vãos/limites** — os defaults de referência
  desta ADR podem ser confirmados/refinados no handoff de implementação.
- **Decidir `corpo.arranjo`** — esta ADR não introduz nem remove valores de
  arranjo; `corpo.arranjo` permanece conforme ADR-0011.
- **Normatizar ocupação vertical da janela** — tratada pela ADR-0013.
- **Migrar `destino_minimo`** — fora de escopo explícito.
- **Resolver `sobreposto` residual** — fora de escopo explícito; aliases
  transicionais permanecem conforme ADR-0011.

---

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Normatizar `distribuicao = "horizontal"` apenas como "linha única horizontal" | Gera o vazio normativo que esta ADR fecha: permitiria truncar/omitir/empilhar como fallback; rejeitado pela auditoria como leitura simplificada |
| Tratar distribuição horizontal da barra como parte de ADR-0011 (`corpo.arranjo`) | Colapsa dois campos distintos (`corpo.arranjo` × `barra_de_menus.distribuicao`) em regiões distintas; já rejeitado pela disambiguação da ADR-0011 |
| Normatizar apenas a Parte A sem qualificar "responsiva" | Deixaria a distribuição sujeita a ser lida como linha única fixa, contrariando o achado bloqueante da auditoria |
| Normatizar apenas a Parte B, sem a Parte A | Deixaria a distribuição horizontal da barra sem norma específica, sujeita a ser lida como alias de arranjo horizontal |
| Migrar agora os JSONs para o objeto canônico (`modo = "horizontal_responsiva"`) | Quebra o princípio de ADR normativa vs. handoff de implementação; a migração de JSON/código/testes é pendência de handoff futuro |
| Implementar a distribuição horizontal agora, na própria ADR | Quebra o princípio de ADR normativa vs. handoff de implementação; a decisão precisa ser aceita antes de o handoff ser escrito |
| Tratar a regra de filtro parcial apenas como nota de rodapé em `contrato_processo_desenvolvimento.md` | A regra é decisão arquitetural (afeta todo o processo documental e toda ADR futura) e merece registro como ADR aceita, não apenas como ajuste de contrato |
