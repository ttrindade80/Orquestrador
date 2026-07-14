# Relatório documental — ADR-0013 e ADR-0014

## Status

DOCUMENTACAO_ATUALIZADA

> **Correção pós-auditoria (QA_REJECTED → reauditoria)**: a auditoria Codex
> (`RELATORIO_AUDITORIA_ADR-0013_ADR-0014.md`, evidência histórica não
> alterada) retornou `QA_REJECTED` com achado bloqueante: a ADR-0014
> normatizava `distribuicao = "horizontal"` apenas como "barra horizontal",
> permitindo leitura simplificada de "linha única simples". A correção
> requalificou `barra_de_menus.distribuicao = "horizontal"` como
> **distribuição horizontal responsiva** (alias transitório de
> `modo = "horizontal_responsiva"`), registrou a estrutura canônica futura
> como objeto declarativo, o algoritmo normativo mínimo, ordem/âncoras,
> overflow determinístico e proibições. Erro textual `levanta mentos` →
> `levantamentos` corrigido na ADR-0014. Ver seção "Correção pós-auditoria"
> abaixo.

## Contexto

O projeto está após o commit `8a6403a feat: migra arranjo vertical e barra
declarativa`, que aplicou a ADR-0011 (terminologia de arranjo
`vertical`/`horizontal`) e a ADR-0012 (`barra_de_menus` declarativa por tela)
em código, JSONs e testes.

Um levantamento técnico/documental em modo somente leitura constatou:

- `tela/demo.py` lê apenas a largura do terminal por
  `shutil.get_terminal_size(...).columns`;
- `tela/renderizador.py` (`renderizar_tela`) recebe apenas `largura`, não
  altura;
- o corpo ocupa largura, mas não preenche altura disponível — não há
  `altura_disponivel`, `rows` nem preenchimento vertical do corpo;
- `barra_de_menus.distribuicao = "horizontal"` está declarado nos JSONs
  ativos (`orquestrador.json`, `destino_minimo.json`, `grupo_minimo.json`,
  `stub_b.json`), mas o renderer (`_linhas_barra`) ignora essa distribuição
  e empilha os chips, criando uma linha por chip;
- a ADR-0012 já fixou a barra como declarativa por tela, mas a **distribuição
  visual horizontal** da barra ainda não havia sido normatizada;
- há risco terminológico porque `vertical`/`horizontal` circulam com três
  significados distintos: `corpo.arranjo` (ADR-0011),
  `barra_de_menus.distribuicao` (ativo) e, futuramente,
  `ocupacao_vertical_terminal` (ADR-0013).

A decisão gerencial foi criar **duas ADRs específicas e autônomas**, para que
uma ADR futura sobre `arranjo vertical/horizontal` não seja lida de forma
ambígua e não sobrescreva/acumule indevidamente estas decisões:

- **ADR-0013** — Ocupação vertical da janela do terminal pelo corpo.
- **ADR-0014** — Distribuição horizontal **responsiva** da `barra_de_menus`
  e alteração por termo específico completo.

Esta tarefa é estritamente documental e normativa. Não altera código, testes,
JSONs de produção, handoffs nem levantamentos. Não cria handoff de
implementação. Não faz commit.

## ADRs criadas

| Arquivo | Conteúdo normativo |
|---|---|
| `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md` | A tela deve ocupar largura **e** altura disponíveis; altura passa a ser dimensão explícita do render; o corpo preenche a área entre `cabecalho` e `barra_de_menus`; preenchimento vertical é responsabilidade do renderer, não do JSON; **não** confundir com `corpo.arranjo`; termo específico `ocupacao_vertical_terminal` (ou `preenchimento_altura_corpo`, `altura_disponivel`); não implementa código nem testes |
| `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` | **Parte A**: `barra_de_menus.distribuicao = "horizontal"` é **distribuição horizontal responsiva** (não linha única fixa); alias transitório de `distribuicao.modo = "horizontal_responsiva"`; estrutura canônica futura como objeto declarativo registrada; algoritmo normativo mínimo; ordem por declaração; âncoras como validação; overflow determinístico; proibições (não empilhar, não omitir/truncar/reordenar); distinto de `corpo.arranjo = "horizontal"`. **Parte B**: filtros parciais só para busca; alterações normativas exigem termo específico completo; proibida substituição por substring ambígua; vale para ADRs, handoffs, implementações, migrações e QAs |

## Documentos atualizados

| Arquivo | Alteração mínima realizada |
|---|---|
| `docs/adr/INDICE_ADR.md` | Adicionadas as linhas de ADR-0013 e ADR-0014 à tabela de decisões registradas; título da ADR-0014 reflete "distribuição horizontal responsiva" |
| `docs/NOMENCLATURA.md` | `atualizado_em` → 2026-07-09; seção 1.4: disambiguação obrigatória — `corpo.arranjo = "vertical"` é composição, não ocupação de altura; `ocupacao_vertical_terminal` como termo específico de preenchimento da altura; seção 5 (`barra_de_menus`): tabela de disambiguação dos três termos — `corpo.arranjo = "horizontal"`, `barra_de_menus.distribuicao = "horizontal"` (alias transitório de responsiva) e `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` (canônico futuro), independentes entre si; regra contra filtro parcial |
| `docs/contratos/contrato_tela_json.md` | Seção 9 (Tiling e posicionamento): nota de ocupação vertical (ADR-0013) — altura disponível como dimensão futura, corpo preenche área vertical, distinção de `corpo.arranjo`; seção 18 (`barra_de_menus`): `barra_de_menus.distribuicao` admite forma transitória (string `"horizontal"`) e canônica futura (objeto com `modo = "horizontal_responsiva"`); string é alias de distribuição horizontal responsiva, não linha única fixa; nota contra filtro parcial |
| `docs/contratos/contrato_composicao_corpo.md` | Frontmatter: ADR-0013 em `adrs_aplicadas`; nova seção 4.7 (Ocupação vertical da janela): tabela de distinção `corpo.arranjo = "vertical"` × `ocupacao_vertical_terminal`/`preenchimento_altura_corpo`; corpo preenche altura disponível com linhas em branco pelo renderer; ocupação vertical não introduz novo arranjo nem altera composição |
| `docs/contratos/contrato_barra_de_menus.md` | Frontmatter: ADR-0014 em `adrs_aplicadas`; seção 17 (Distribuição e ordem de instância): regra normativa completa — `distribuicao = "horizontal"` como alias transitório de `modo = "horizontal_responsiva"` (distribuição horizontal responsiva, não linha única fixa); formato canônico futuro como objeto declarativo; tentativa de linha única, quebra multilinha, preenchimento declarado; vãos mínimos/máximos; ordem por declaração; âncoras como validação; overflow determinístico; proibição de empilhar um chip por linha e de omitir/truncar/reordenar para caber; distinto de `corpo.arranjo = "horizontal"`; chips de `lancador`/corpo não são chips da barra |
| `docs/contratos/contrato_processo_desenvolvimento.md` | Nova seção 10 (Alteração por termo específico completo — ADR-0014): filtros parciais só para busca; alterações normativas e implementações atingem apenas termos específicos completos; ADRs/handoffs declaram campo/conceito afetado; auditorias bloqueiam substituição por substring ambígua; regra vale para ADRs/handoffs/implementações/migrações/QAs |

### Documento avaliado e mantido inalterado

| Arquivo | Motivo de não alterar |
|---|---|
| `docs/contratos/contrato_json_tela_minima.md` | Avaliado conforme orientação: não contém exemplos que confundam arranjo vertical com ocupação vertical nem com distribuição horizontal da barra. O exemplo `"arranjo": "vertical"` da seção 4.1 refere-se corretamente à composição (`corpo.arranjo`, ADR-0011). ADR-0013 não lista este contrato em `contratos_afetados`; logo, o frontmatter também permanece inalterado |

## Decisões registradas

### ADR-0013 — Ocupação vertical da janela do terminal pelo corpo

1. A tela textual deve ocupar a largura e a altura disponíveis da janela do
   terminal.
2. A largura já é tratada dinamicamente; a altura deve passar a ser tratada
   como dimensão explícita do render.
3. O corpo deve ocupar a altura disponível entre `cabecalho` e
   `barra_de_menus`.
4. Quando o conteúdo funcional do corpo não ocupar toda a altura disponível,
   o renderer deve preencher o espaço restante com linhas em branco.
5. O preenchimento vertical do corpo é responsabilidade do renderer, não do
   JSON.
6. A decisão não altera a semântica de `corpo.arranjo`.
7. `corpo.arranjo = "vertical"` significa ordem/composição vertical dos
   elementos, não ocupação da altura do terminal.
8. A ocupação vertical da janela deve usar termo específico, por exemplo
   `ocupacao_vertical_terminal`, `preenchimento_altura_corpo`,
   `altura_disponivel`.
9. O handoff futuro que implementar essa ADR decide a representação exata
   das linhas de preenchimento (linha visual interna vs. linha física
   total), mas sem confundir isso com arranjo de composição.
10. Esta ADR não implementa código nem altera testes agora.

### ADR-0014 — `barra_de_menus` horizontal responsiva e termos específicos

**Parte A — `barra_de_menus.distribuicao = "horizontal"` é distribuição
horizontal responsiva**

1. A `barra_de_menus` continua declarativa por tela (ADR-0012).
2. A distribuição visual da barra é controlada por termo específico
   `barra_de_menus.distribuicao`.
3. `barra_de_menus.distribuicao = "horizontal"` **não** significa linha
   única fixa; significa **distribuição horizontal responsiva**.
4. A string `"horizontal"` é formato **transitório** (alias de
   `distribuicao.modo = "horizontal_responsiva"`).
5. O formato canônico futuro é objeto declarativo:
   `barra_de_menus.distribuicao.modo = "horizontal_responsiva"`.
6. O renderer deve respeitar a distribuição declarada na instância.
7. O renderer não deve empilhar um chip por linha quando a distribuição
   declarada for horizontal/horizontal_responsiva.
8. O renderer não deve reordenar chips por heurística própria.
9. O renderer não deve inventar chips ausentes.
10. O renderer não deve completar a barra com a lista canônica global.
11. O renderer não deve transformar erro de layout em omissão silenciosa de
    chip.
12. A `barra_de_menus` não herda regra do `lancador`.
13. Chips de itens do `lancador` não são chips da `barra_de_menus`.
14. A ordem de exibição dos chips é a ordem declarada em
    `barra_de_menus.chips[]`, salvo política explícita de
    agrupamento/âncoras.
15. A distribuição da `barra_de_menus` é independente de
    `corpo.arranjo = "horizontal"`.
16. Esta ADR não implementa código, não altera JSON e não altera testes
    agora.

A Parte A registra ainda: estrutura canônica futura como objeto declarativo;
campos e semânticas (`modo`, `tentativa_inicial`, `quebra`,
`preenchimento_multilinha`, `ordem.politica`, `linhas`, `alinhamento_linhas`,
`espacamentos`, `colunas`, `overflow`); algoritmo normativo mínimo;
ordem/âncoras como validação; overflow determinístico; proibições explícitas;
e compatibilidade transitória da string `"horizontal"`.

**Parte B — regra de alteração por termo específico completo**

1. Filtros parciais podem ser usados para busca, auditoria e localização.
2. Filtros parciais NÃO podem ser usados como critério de alteração
   normativa automática.
3. ADRs, contratos, JSONs, código e testes só podem ser alterados quando o
   termo específico completo afetado for identificado.
4. É proibido aplicar uma decisão procurando apenas substrings ambíguas
   (`vertical`, `horizontal`, `barra`, `chip`, `arranjo`).
5. Toda ADR deve indicar o termo específico completo que está alterando.
6. Exemplos de termos específicos completos: `corpo.arranjo = "vertical"`,
   `corpo.arranjo = "horizontal"`, `barra_de_menus.distribuicao = "horizontal"`,
   `barra_de_menus.distribuicao.modo = "horizontal_responsiva"`,
   `ocupacao_vertical_terminal`, `preenchimento_altura_corpo`,
   `chip canônico`, `chip declarado por tela`.
7. A busca por termo parcial pode aparecer em levantamento/auditoria, mas a
   aplicação da alteração deve ser revisada termo a termo.
8. Esta regra vale para ADRs futuras, handoffs, implementações, migrações e
   QAs.

## Distinções terminológicas preservadas

- **`corpo.arranjo = "vertical"`** — ordem/composição vertical dos elementos
  do corpo (ADR-0011).
- **`ocupacao_vertical_terminal`** — preenchimento da altura da janela do
  terminal pela tela (ADR-0013).
- **`preenchimento_altura_corpo`** — linhas em branco adicionadas pelo
  renderer para ocupar a altura do corpo (ADR-0013).
- **`barra_de_menus.distribuicao = "horizontal"`** — distribuição horizontal
  **responsiva** dos chips na região da barra; alias transitório de
  `distribuicao.modo = "horizontal_responsiva"` (ADR-0014, Parte A).
- **`barra_de_menus.distribuicao.modo = "horizontal_responsiva"`** — formato
  canônico futuro da distribuição responsiva dos chips, objeto declarativo
  (ADR-0014, Parte A).
- **`corpo.arranjo = "horizontal"`** — ordem/composição horizontal dos
  elementos do corpo (ADR-0011).

Estas distinções são **independentes e não colapsam**: uma substring
(`vertical`, `horizontal`) não identifica unicamente o campo/conceito. ADRs,
handoffs, implementações, migrações e auditorias devem referir-se a cada um
pelo termo específico completo.

## Regra contra alteração por filtro parcial

Registrada formalmente em:

- `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` (Parte B);
- `docs/NOMENCLATURA.md` (seção 5);
- `docs/contratos/contrato_tela_json.md` (seção 18);
- `docs/contratos/contrato_processo_desenvolvimento.md` (nova seção 10).

Síntese: filtros parciais por substring são permitidos apenas para
busca/auditoria; a alteração normativa e de implementação deve atingir apenas
termos específicos completos, identificados e confirmados termo a termo;
substituição global por substring ambígua é proibida; auditorias devem
bloqueá-la quando houver ambiguidade.

## Correção pós-auditoria (QA_REJECTED → reauditoria)

A auditoria Codex (`docs/relatorios/RELATORIO_AUDITORIA_ADR-0013_ADR-0014.md`,
mantida intacta como evidência histórica) retornou `QA_REJECTED` com:

**Achado bloqueante (1):** a ADR-0014 normatizava `distribuicao =
"horizontal"` apenas como "barra horizontal", o que impede o empilhamento
simples (um chip por linha), mas ainda permitia a interpretação
simplificada de "todos os chips em uma única linha".

**Achado não bloqueante (2):** pequeno erro textual `levanta mentos` na
ADR-0014; parâmetros quantitativos podem ficar para handoff futuro se a
responsividade for normatizada.

### Correção aplicada

Para fechar o achado bloqueante, a documentação foi corrigida para
requalificar `barra_de_menus.distribuicao = "horizontal"` como
**distribuição horizontal responsiva** (não linha única fixa):

- **ADR-0014** reescrita: título passa a "Distribuição horizontal responsiva
  da `barra_de_menus` e termos específicos"; Parte A registra as 16 decisões
  (não é linha única fixa; é responsiva; `"horizontal"` é alias transitório;
  formato canônico futuro é objeto com `modo = "horizontal_responsiva"`;
  renderer respeita a declaração; não empilha/reordena/inventa/completa;
  erro de layout não vira omissão; barra não herda regra do `lancador`;
  chips de `lancador` não são da barra; ordem por declaração; independente
  de `corpo.arranjo`; não implementa código/JSON/testes), a estrutura
  canônica futura como objeto declarativo, os campos e semânticas, o
  algoritmo normativo mínimo, a seção de ordem e âncoras, a seção de
  overflow, a seção de proibições e a compatibilidade transitória.
- **`contrato_barra_de_menus.md`** (seção 17): regra normativa completa
  (alias transitório; objeto canônico futuro; tentativa de linha única;
  quebra multilinha; preenchimento declarado; vãos; ordem por declaração;
  âncoras como validação; overflow determinístico; proibições).
- **`contrato_tela_json.md`** (seção 18): `barra_de_menus.distribuicao`
  admite forma transitória (string) e canônica futura (objeto); string é
  alias de responsiva.
- **`NOMENCLATURA.md`** (seção 5): tabela de disambiguação dos três termos
  independentes.
- **`INDICE_ADR.md`**: título da ADR-0014 reflete "distribuição horizontal
  responsiva".
- **Erro textual** `levanta mentos` → `levantamentos` corrigido na
  ADR-0014 (a ocorrência no relatório de auditoria permanece como
  evidência histórica, não alterada).

Parâmetros quantitativos finais (vãos, limites de linhas) permanecem como
defaults de referência na ADR-0014, refináveis no handoff futuro de
implementação — não decididos nesta correção.

## Fora de escopo preservado

- **Código não alterado**: `tela/` intacto.
- **JSONs não alterados**: `config/` intacto.
- **Testes não alterados**: nenhum arquivo de teste tocado.
- **Handoffs não criados nem alterados**: `docs/handoff/` intacto; em
  particular, **H-0015 não foi iniciado** e nenhum handoff de implementação
  das ADRs foi criado.
- **Levantamentos e relatórios prévios não alterados**:
  `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`
  permanece somente leitura; `IMP-0014-*`, `RELATORIO_QA_H-0014_*` e demais
  relatórios prévios permanecem intactos.
- **ADR-0011 e ADR-0012 não alteradas**: suas semânticas são preservadas e
  ampliadas (não contraditas) por ADR-0013 e ADR-0014.
- **`corpo.arranjo` não alterado**: nenhum valor de arranjo foi adicionado
  ou removido; aliases transicionais (`sobreposto`/`lado_a_lado`) permanecem
  conforme ADR-0011.
- **`destino_minimo` não migrado**: fora de escopo explícito.
- **`sobreposto` residual não resolvido**: fora de escopo explícito.
- **Representação final das linhas em branco não decidida no código**:
  decisão adiada para handoff futuro de implementação da ADR-0013.
- **Renderização horizontal responsiva da barra não implementada**: o
  renderer ainda empilha um chip por linha; pendência de handoff futuro.
  A ADR-0014 fecha a norma (responsiva, não linha única fixa) — não
  implementa.
- **JSONs não migrados para o formato canônico**: os JSONs ativos
  permanecem com `"distribuicao": "horizontal"` (string); a migração para
  o objeto declarativo (`modo = "horizontal_responsiva"`) é pendência de
  handoff futuro.
- **Altura dinâmica não implementada**: pendência de handoff futuro.
- **`contrato_json_tela_minima.md` não alterado**: avaliado e mantido
  inalterado (não confunde arranjo/ocupação/distribuição).
- **Nenhum commit realizado**.

## Pendências futuras

- **Implementação da ocupação vertical do terminal** (ADR-0013): propagar
  `.lines` do terminal até `renderizar_tela`, calcular `altura_disponivel`
  entre `cabecalho` e `barra_de_menus`, e implementar o preenchimento
  vertical do corpo.
- **Decisão sobre a representação das linhas de preenchimento** (linha
  visual interna à caixa do corpo vs. linha física com largura total) —
  adiada para o handoff de implementação da ADR-0013.
- **Implementação da distribuição horizontal responsiva da `barra_de_menus`**
  (ADR-0014, Parte A): fazer o renderer respeitar
  `barra_de_menus.distribuicao = "horizontal"` (alias) /
  `distribuicao.modo = "horizontal_responsiva"` (canônico) em vez de
  empilhar um chip por linha, seguindo o algoritmo normativo mínimo da
  ADR-0014 (tentativa de linha única, quebra multilinha determinística,
  preenchimento declarado, erro de layout determinístico quando nenhum
  arranjo couber).
- **Migração dos JSONs ativos** do formato string `"horizontal"` para o
  formato canônico objeto (`modo = "horizontal_responsiva"`) — pendência de
  handoff futuro; os JSONs de produção permanecem com o formato string.
- **Decisão sobre a regra de quebra de linha da barra horizontal** quando
  os chips excederem a largura disponível — normatizada como multilinha
  determinística pela ADR-0014; detalhes finais no handoff futuro.
- **Testes de altura disponível** e de preenchimento vertical do corpo.
- **Testes de barra horizontal responsiva** (linha única quando couber;
  multilinha determinística quando não couber; erro de layout determinístico
  quando nenhum arranjo couber).
- **Handoff futuro para aplicação das ADRs** (H-0015 ou subsequente), com
  escopo restrito a `tela/` e `config/`, e termos específicos completos
  declarados.

## Verificações

Comandos executados para confirmar o escopo documental:

```text
$ git status --short
$ git diff --stat
$ git diff --name-only
```

Resultados capturados na seção "git_status" abaixo.

Confirmação de preservação de escopo:

- Nenhuma alteração em `config/` (sem `config/...` em `git status`/`git diff`).
- Nenhuma alteração em `tela/` (sem `tela/...` em `git status`/`git diff`).
- Nenhuma alteração em `docs/handoff/`.

Nota: este relatório
(`docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0013_ADR-0014.md`) passa a constar
como não rastreado após sua criação, junto aos dois arquivos de ADR criados.
