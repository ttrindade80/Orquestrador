---
name: ADR-0007-tela-processamento-composicao
description: tela de processamento não é quarto tipo de corpo; deve ser modelada como composição de console, dashboard e chips específicos da barra_de_menus
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
  handoffs_bloqueados: []
---

# ADR-0007 — tela de processamento é composição de tipos existentes

## Status

`aceita`

## Data

2026-07-06

## Contexto

A ADR-0006 fechou a taxonomia do corpo em três tipos — `console`, `lancador` e `dashboard` — e
declarou explicitamente (decisão 11) que telas de processamento não têm tipo de corpo definido por
aquela decisão, cabendo tratamento em decisão própria ou como composição dos tipos existentes.

Antes de abrir contratos detalhados para telas de processamento, é necessário registrar formalmente
se elas constituem um quarto tipo de corpo ou se devem ser especificadas como composição dos tipos
já existentes.

A questão se torna relevante porque telas de processamento apresentam simultaneamente:
- uma região interativa/navegável (lista de itens processados, log navegável, detalhes);
- uma região de saída passiva formatada (estado agregado, contadores, progresso, legenda);
- ações específicas da classe (chips que não existem em telas de outro tipo).

A taxonomia vigente já contempla exatamente esses três papéis: `console` (interativo/navegável),
`dashboard` (saída passiva), e chips específicos da `barra_de_menus`. Criar um quarto tipo seria
duplicar responsabilidades já cobertas, aumentar a superfície normativa sem necessidade, e
introduzir ambiguidade sobre quando usar o novo tipo versus os três existentes.

## Decisão

As seguintes declarações constituem a decisão formal desta ADR:

**1. Tela de processamento não é quarto tipo de corpo.**
A existência de uma tela cujo fluxo principal é um processo em execução não justifica a criação de
novo tipo de objeto do corpo. O comportamento observado em telas de processamento é inteiramente
expressável pelos tipos já definidos.

**2. A taxonomia fechada do corpo permanece: `console`, `lancador`, `dashboard`.**

| Tipo | Natureza | Navegável por `[✥]` |
|---|---|---|
| `console` | corpo interativo com cursor, seleção e ações | sim |
| `lancador` | corpo de navegação por itens para outras telas | não |
| `dashboard` | saída passiva formatada — painel de leitura | não |

Nenhum outro tipo existe na taxonomia. Extensões futuras exigem nova ADR.

**3. Uma tela de processamento deve ser especificada como composição de tipos existentes.**
A classe de tela declara os tipos de objeto do corpo que a compõem, conforme as regras de
`contrato_composicao_corpo.md`. Para uma tela de processamento, a composição envolve um ou mais
`console`, zero ou um `dashboard`, e chips específicos declarados na `barra_de_menus`.

**4. `console` representa a região interativa/navegável por `[✥]` da tela de processamento.**
Qualquer região da tela de processamento que expõe cursor navegável — listas de itens, alvos,
logs navegáveis ou detalhes navegáveis — deve ser especificada como `console`. As regras de
navegação por `[✥]`, estrutura de item `ec`/`tg`/`tx`, `tipo_exibicao`, `paginacao`,
`colunas_ajustavel` e `formacao_de_selecao` se aplicam normalmente.

**5. `dashboard` representa a saída passiva formatada da tela de processamento.**
Qualquer região da tela de processamento que exibe estado agregado, resumo, contadores, progresso
ou legenda — sem expor cursor navegável — deve ser especificada como `dashboard`. As regras de
`dashboard` (saída passiva, não navegável por `[✥]`) se aplicam normalmente.

**6. Chips específicos da `barra_de_menus` representam ações próprias da classe de tela de processamento.**
Uma classe de tela de processamento pode declarar chips que não existem em outras classes (por
exemplo, um chip que aciona ou interrompe o processo). Esses chips são chips específicos, distintos
dos chips canônicos da `barra_de_menus`.

**7. Chips específicos continuam pertencendo à `barra_de_menus`, não ao corpo.**
A presença de chips específicos em uma tela de processamento não altera a separação fundamental
entre `barra_de_menus` (região fixa da tela) e corpo. O chip existe na `barra_de_menus`; o `console`
e o `dashboard` existem no corpo. Essa separação é invariante.

**8. A existência de chips específicos deve ser declarada pela classe de tela.**
A classe de tela de processamento é responsável por declarar quais chips específicos existem na
sua `barra_de_menus`. A `barra_de_menus` é espelho da declaração da classe — não é a fonte da
decisão. Esta regra é consistente com o princípio geral do `contrato_barra_de_menus.md`.

**9. `lancador` não é usado para representar processamento.**
`lancador` é um objeto do corpo que agrupa itens de navegação para outras telas via `tela_destino`.
Seu papel é estruturalmente diferente do papel de qualquer parte de uma tela de processamento.
Uma tela de processamento não deve incluir `lancador` como representação do processo em si.
As regras do `lancador` (ADR-0005, `contrato_lancador.md`) permanecem inalteradas.

**10. Nenhuma decisão desta ADR altera as regras de `[✥]`.**
Somente `console` é navegável por `[✥]`. Esta regra, estabelecida nas ADR-0005 e ADR-0006, não é
afetada pela composição descrita nesta ADR. Se uma tela de processamento possui um `console`, as
setas da `barra_de_menus` navegam o cursor desse `console` — exatamente como em qualquer outra
tela que contenha um `console`.

## Composição conceitual

O exemplo a seguir ilustra uma tela de processamento possível. Não é um contrato — não cria
obrigação universal de estrutura.

Uma tela de processamento pode conter:

- `cabeçalho` (título e descrição da classe, conforme `contrato_cabecalho.md`);
- corpo com um ou mais `console`, por exemplo:
  - `console` Lista — itens a processar ou já processados, navegável por `[✥]`;
  - `console` Detalhe — detalhes do item selecionado, navegável por `[✥]`;
  - `console` Log — saída de log, se o log for navegável;
- zero ou um `dashboard` — por exemplo estado agregado do processo (contadores, progresso, legenda);
- `barra_de_menus` com chips canônicos e chips específicos da classe (por exemplo, um chip que
  aciona ou interrompe o processo).

Uma tela de processamento pode ter apenas `console` sem `dashboard`, apenas `dashboard` sem
`console`, ou a combinação dos dois — a composição é declarada pela classe. O que esta ADR veda
é criar um tipo de corpo novo para denominar essa composição.

## Consequências

### Artefatos a atualizar em próxima tarefa

A aplicação desta ADR exige que uma tarefa separada atualize, no mínimo:

| Arquivo | Atualização necessária |
|---|---|
| `docs/NOMENCLATURA.md` | Registrar que tela de processamento é composição de `console` + `dashboard` + chips específicos; não criar nova entrada de tipo de corpo |
| `docs/contratos/contrato_composicao_corpo.md` | Adicionar seção ou nota sobre tela de processamento como composição; confirmar que a taxonomia permanece fechada |
| `docs/contratos/contrato_barra_de_menus.md` | Confirmar/clarificar regra de chips específicos declarados pela classe de tela; se houver impacto para telas de processamento |
| `docs/build_docs/to_do.md` | Registrar próxima tarefa de aplicação desta ADR |

**Esta tarefa (DOC-0013) não altera esses artefatos.**

### Arquivos que não devem ser alterados por esta decisão

| Arquivo | Motivo |
|---|---|
| `docs/contratos/contrato_lancador.md` | `lancador` permanece com as mesmas regras |
| `docs/contratos/contrato_estilo.md` | Não referencia tipos de corpo por composição |
| `docs/contratos/contrato_cabecalho.md` | Fora do escopo — `cabecalho` não é tipo de corpo |
| `config/*.json` | Implementação aguarda contratos atualizados |
| Qualquer arquivo de código | Implementação aguarda contratos atualizados |
| Qualquer arquivo em `docs/relatorios/` | Não é normativo; não cria regra |

## Fora de escopo

Os pontos abaixo não são decididos por esta ADR:

- Contrato detalhado de tela de processamento.
- Pop-up de ferramenta (`popup_execucao`).
- Seleção prévia de ferramenta.
- Execução em segundo plano.
- Estrutura do chip específico `aciona_processo`.
- Implementação em código.
- Alteração de dados reais de classes/telas.
- Decisão sobre processo assíncrono.
- Renderer de progresso.
- Handoff de implementação.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Criar quarto tipo de corpo `processamento` | Duplica responsabilidades já cobertas por `console` e `dashboard`; aumenta a superfície normativa sem benefício; introduz ambiguidade na taxonomia fechada |
| Tratar telas de processamento como variante de `console` | `console` é um objeto do corpo — não uma tela; mistura os níveis de abstração |
| Adiar a decisão sem registrar ADR | Deixaria o princípio de composição implícito; futuros contratos poderiam derivar na direção errada de criar novo tipo |
