---
name: ADR-0006-renomeacao-console-dashboard
description: dado passa a se chamar console; Info passa a se chamar dashboard; taxonomia fechada do corpo é console, lancador, dashboard
metadata:
  type: adr
  status: aceita
  data: 2026-07-06
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/NOMENCLATURA.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - config/barra_de_menus.json
    - config/layout_dado.json
  handoffs_bloqueados: []
---

# ADR-0006 — renomeação `dado` para `console` e `Info` para `dashboard`

## Status

`aceita`

## Data

2026-07-06

## Contexto

Após a consolidação da taxonomia do corpo com o `lancador` (DOC-0008, DOC-0009) e a restrição de
`[✥]` a corpo tipo `dado` (ADR-0005), dois dos três tipos de objeto do corpo mantinham nomes que
não expressavam adequadamente sua natureza semântica no sistema:

- **`dado`**: nome demasiado genérico para um tipo de corpo interativo/navegável. O termo `dado`
  poderia referir-se a qualquer dado exibido, criando ambiguidade com o próprio conteúdo exibido
  em outros tipos de corpo. O nome `console` expressa melhor o papel do tipo: um espaço de
  interação ativa com dados — navegação, seleção, execução.

- **`Info`** (com inicial maiúscula): nome informal herdado de prática anterior. O objeto `Info`
  é uma saída passiva formatada — um painel de resumo/legenda. O nome `dashboard` expressa melhor
  esse papel: uma visão consolidada de leitura, sem interação pelo usuário.

O terceiro tipo, `lancador`, não apresenta ambiguidade e permanece inalterado.

Nota de rastreabilidade: a ADR-0005 já antecipou que a renomeação `dado` → `console` seria
registrada em decisão própria e usou o termo `dado` como nomenclatura vigente à época. Esta ADR
é a decisão própria mencionada.

## Decisão

As seguintes declarações constituem a decisão formal desta ADR:

**1. O antigo tipo de corpo `dado` passa a ser chamado formalmente de `console`.**
`console` é o nome canônico a partir desta decisão. O nome `dado` é descontinuado como nome
de tipo — pode aparecer em artefatos históricos por rastreabilidade, mas não deve ser usado em
novas decisões, contratos ou configurações.

**2. `console` preserva integralmente as regras do antigo `dado`.**
A renomeação não altera nenhuma regra aprovada para o antigo `dado`:

- `console` é corpo interativo e navegável por `[✥]` (setas do teclado controlam o cursor interno).
- A estrutura de item de `console` é `ec` / `tg` / `tx` (espaço do cursor, espaço de toggle, texto).
- `console` pode declarar `tipo_exibicao` (`normal` ou `verboso`), `colunas_ajustavel` (`com`/`sem`),
  `paginacao` (`com`/`sem`) e `formacao_de_selecao` (`com`/`sem`) — eixos já definidos.
- Os chips `[✥]`, `[-][+]`, `[<][>]`, `[V]`, `[␣]` vinculados ao antigo `dado` continuam
  vinculados ao `console` com as mesmas regras de existência e estado dinâmico.

**3. A renomeação `dado` → `console` é terminológica e taxonômica.**
Não muda regras, não muda comportamentos, não muda estrutura de item. Muda apenas o nome do tipo.
Ajustes de nome em artefatos existentes são obrigatórios na próxima tarefa, mas não constituem
alteração de regra.

**4. O antigo objeto `Info` passa a ser chamado formalmente de `dashboard`.**
`dashboard` é o nome canônico a partir desta decisão. O nome `Info` (com inicial maiúscula ou
minúscula) é descontinuado como nome de tipo — pode aparecer em artefatos históricos por
rastreabilidade, mas não deve ser usado em novas decisões.

**5. `dashboard` é saída passiva formatada; não é corpo interativo e não é navegável por `[✥]`.**
O papel do `dashboard` é exibir um painel de leitura — resumo, legenda ou vista consolidada dos
dados do contexto. O usuário lê, não interage. O chip `[✥]` e as setas da `barra_de_menus` não
consideram `dashboard` como condição de existência nem de ativação, assim como já não consideravam
o antigo `Info`.

**6. `dashboard` não deve ser definido universalmente pela estrutura de 8 campos + 8 marcadores do antigo `Info`.**
A estrutura descrita em `docs/NOMENCLATURA.md` seção 9 (8 campos de resumo + Total + 8 marcadores
com símbolo/rótulo/valor) é um caso específico ou exemplo legado do sistema de survey em
desenvolvimento — não é uma regra universal do tipo `dashboard`. Outros usos do tipo `dashboard`
podem ter estrutura diferente. Contratos futuros de `dashboard` devem tratar essa estrutura como
instância, não como definição universal do tipo.

**7. `lancador` permanece com o mesmo nome e com a mesma regra.**
O tipo de objeto do corpo `lancador` não é afetado por esta decisão. Suas regras permanecem
integralmente conforme ADR-0005 e `contrato_lancador.md`:

- Composição de navegação por itens próprios via `tela_destino`.
- Não é corpo navegável por `[✥]` nem pelas setas da `barra_de_menus`.
- Estrutura de item: `chip` + `texto` (máx. 15 caracteres) + `tela_destino`.

**8. A taxonomia fechada do corpo passa a ser: `console`, `lancador`, `dashboard`.**

| Tipo | Natureza | Navegável por `[✥]` |
|---|---|---|
| `console` | corpo interativo com cursor, seleção e ações | sim |
| `lancador` | corpo de navegação por itens para outras telas | não |
| `dashboard` | saída passiva formatada — painel de leitura | não |

Nenhum outro tipo existe na taxonomia atual. Extensões futuras exigem nova ADR.

**9. Após esta ADR, substituição obrigatória de referências ativas.**
A próxima tarefa de aplicação deverá:

- Substituir `dado` por `console` em todos os artefatos normativos ativos
  (`NOMENCLATURA.md`, contratos, configs).
- Substituir `Info` por `dashboard` nos mesmos artefatos.
- Preservar os nomes antigos somente quando o contexto for explicitamente histórico ou de
  rastreabilidade (ex.: "o antigo `dado`", "antes chamado `Info`").

**10. A regra de `[✥]` deverá ser atualizada de "corpo tipo `dado`" para "corpo tipo `console`".**
Todos os artefatos que condicionam a existência ou ativação de `[✥]` ao tipo `dado` deverão
trocar essa referência para `console`. O comportamento não muda — só o nome do tipo referenciado.
Esta atualização será executada na mesma tarefa de aplicação da renomeação.

**11. Esta ADR não cria novo tipo de corpo para telas de processamento.**
Telas cujo fluxo principal é um processo em execução (script, operação longa, feedback em tempo
real) não têm tipo de corpo definido por esta decisão. Qualquer tratamento dessas telas deverá
ser feito em decisão própria ou como composição dos tipos existentes (`console`, `lancador`,
`dashboard`).

**12. Esta tarefa (DOC-0011) não aplica a renomeação nos contratos/configs.**
Apenas registra a decisão. A aplicação efetiva é a próxima tarefa.

## Consequências

### Artefatos a corrigir em tarefa subsequente

Os arquivos abaixo devem ser atualizados por uma tarefa separada, após aceite desta ADR.
**Esta tarefa (DOC-0011) não altera esses arquivos.**

| Arquivo | Correção necessária |
|---|---|
| `docs/NOMENCLATURA.md` | Substituir `dado` por `console` e `Info` por `dashboard` em toda seção normativa; atualizar tabela de tipos (seção 2.1), eixos (seção 3), mecanismos de seleção (seção 4), `[✥]` (seção 4.1 e 5.1), seção 9 |
| `docs/contratos/contrato_composicao_corpo.md` | Substituir `dado` por `console` e `Info` por `dashboard` na taxonomia, nas regras e nos critérios de aceite |
| `docs/contratos/contrato_barra_de_menus.md` | Atualizar chip `[✥]`: trocar referência a "corpo tipo `dado`" por "corpo tipo `console`" |
| `config/barra_de_menus.json` | Chip `navegar`, campo `existencia`: trocar referência a `dado` por `console` |
| `config/layout_dado.json` | Atualizar campo `_meta.name` e `_meta.description` para refletir `console`; decidir se o arquivo será renomeado para `config/layout_console.json` ou se a transição será marcada internamente |
| `docs/INDICE.md` | Verificar se lista nomes de configs ou contratos afetados e atualizar se necessário |

### Arquivos que não devem ser alterados por esta decisão

| Arquivo | Motivo |
|---|---|
| `config/lancador.json` | `lancador` permanece — nenhuma alteração de nome ou regra |
| `docs/contratos/contrato_lancador.md` | `lancador` permanece — nenhuma alteração necessária |
| `docs/contratos/contrato_estilo.md` | Não referencia os tipos de corpo por nome de tipo |
| `docs/contratos/contrato_cabecalho.md` | Fora do escopo — `cabecalho` não é tipo de corpo |
| Qualquer arquivo de código | Implementação aguarda contratos e configs corrigidos |
| Qualquer arquivo em `docs/relatorios/` | Não é normativo; não cria regra |

## Fora do escopo desta ADR

Os pontos abaixo não são decididos por esta ADR. Podem ser citados como pendências futuras:

- Contrato de tela de processamento (tipo de corpo para execução de script/operação longa).
- Pop-up de ferramenta (`popup_execucao` — ver `docs/NOMENCLATURA.md` seção 11).
- Execução em segundo plano.
- Estrutura do chip específico `aciona_processo`.
- Renomeação física obrigatória de `config/layout_dado.json` para `config/layout_console.json`
  — esta ADR não impõe nem proíbe a renomeação; a decisão sobre o arquivo fica para a tarefa
  de aplicação.
- Implementação em código.
- Alteração de dados reais de classes/telas.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Manter `dado` e `Info` como nomes canônicos | `dado` é ambíguo com qualquer dado exibido; `Info` é informal e sem expressividade semântica |
| Renomear somente `dado` → `console`, manter `Info` | A mesma lógica de clareza terminológica se aplica; tratar ambos juntos evita um segundo ciclo de decisão |
| Criar subtipo `console` dentro de `dado` em vez de renomear | Introduz hierarquia não necessária; o tipo é o mesmo — só o nome muda |
| Universalizar `dashboard` pela estrutura de 8 campos + 8 marcadores | Engessaria o tipo por uma instância de uso específico do sistema de survey; `dashboard` deve ser mais amplo |
