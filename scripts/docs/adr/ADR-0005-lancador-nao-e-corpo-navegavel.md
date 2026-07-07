---
name: ADR-0005-lancador-nao-e-corpo-navegavel
description: lancador não é corpo navegável por [✥] nem pelas setas da barra_de_menus; [✥] se restringe a corpo tipo dado na etapa atual
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
  handoffs_bloqueados: []
---

# ADR-0005 — lancador não é corpo navegável por [✥]

## Status

`aceita`

## Contexto

Após a formalização do contrato do `lancador` (DOC-0008) e a migração terminológica de `menu` para
`lancador` (DOC-0009), um conjunto de artefatos ativos passou a declarar o `lancador` como "corpo
navegável" no sentido de `[✥]` — isto é, como objeto cujos itens são percorridos pelas setas do
teclado da mesma forma que os itens de um corpo tipo `dado`.

As ocorrências identificadas nos artefatos vigentes:

| Artefato | Trecho problemático |
|---|---|
| `docs/NOMENCLATURA.md` (seção 5.1, tabela de chips) | `[✥]` condição: "tela possui ao menos um corpo navegável (tipo `dado` ou `lancador`)" |
| `docs/contratos/contrato_composicao_corpo.md` (seção 5.2) | "lancador é corpo navegável" |
| `config/barra_de_menus.json` (chip `navegar`, campo `existencia`) | "tipo dado ou menu" |

Nota: `contrato_barra_de_menus.md` (seção 6.3) usa a expressão "tela possui ao menos um corpo
navegável" sem nomear os tipos — o problema é que os artefatos acima, que dão base a esse contrato,
incluem `lancador` (ou seu antigo nome `menu`) como corpo navegável por `[✥]`.

O `lancador` tem uma mecânica interna que envolve posicionamento e seleção de itens (wrap toroidal
registrado em `config/lancador.json`), mas isso é diferente da navegação por `[✥]` do cursor de
`dado`. O `lancador` fornece navegação para outras telas via `tela_destino`; ele não é um objeto
cujo cursor interno é movido pelas setas controladas pela `barra_de_menus`.

Também foi identificada a necessidade de registrar explicitamente que `Info` não é corpo navegável
por `[✥]`, e que a futura renomeação `dado` → `console` (não decidida) não deve ser antecipada
nesta tarefa.

## Decisão

As seguintes declarações constituem a decisão formal desta ADR:

**1. `lancador` é objeto do corpo que aciona navegação por itens próprios, via `tela_destino`.**
O papel do `lancador` é abrir telas — não expor um cursor navegável pelas setas do teclado. Cada
item do `lancador` aponta para uma tela de destino; o acionamento é direto pelo chip do item, não
por cursor posicionado via `[✥]`.

**2. `lancador` não é corpo navegável por `[✥]` nem pelas setas da `barra_de_menus`.**
O chip `[✥]` e as setas do teclado controlam o cursor de um corpo tipo `dado`. O `lancador` não
expõe cursor navegável nesse sentido. O renderer da `barra_de_menus` não deve considerar o
`lancador` como condição de existência ou de ativação de `[✥]`.

**3. Na etapa atual, a condição de existência e ativação de `[✥]` considera somente corpo tipo `dado`.**
A existência estrutural de `[✥]` em uma tela é condicionada à presença de ao menos um corpo tipo
`dado`. A ativação (ativo/inativo) de `[✥]` depende de o corpo tipo `dado` estar em foco. Nenhum
outro tipo de objeto do corpo — nem `lancador`, nem `Info` — participa dessa condição na etapa
atual.

**4. A futura renomeação `dado` → `console` não deve ser aplicada nesta tarefa.**
Se e quando essa renomeação for decidida, será registrada em ADR/tarefa própria. Os artefatos
corrigidos por esta ADR usam o termo `dado` — correto na nomenclatura vigente.

**5. Quando um texto ativo disser "tipo `dado` ou `menu`" ou "tipo `dado` ou `lancador`" no contexto de `[✥]`, a correção futura não é trocar `menu` por `lancador`; é remover `menu`/`lancador` e restringir a `dado`.**
A lógica errada não está no nome do tipo — está em incluir qualquer tipo além de `dado`. A tarefa
de correção deve suprimir a referência ao segundo tipo, não substituí-la.

**6. A mecânica interna do `lancador` registrada em `config/lancador.json` não autoriza o uso de `[✥]`.**
O campo `navegacao` de `config/lancador.json` (wrap toroidal, célula vazia) descreve uma mecânica
própria do `lancador` — não é navegação por `[✥]`. Essa mecânica interna será tratada como assunto
do próprio `lancador` até que uma decisão específica posterior defina se e como ela se integra com
a `barra_de_menus`. Esta ADR não altera nem invalida o campo `navegacao` de `config/lancador.json`.

**7. `Info` não é corpo navegável por `[✥]`.**
O objeto `Info` é um resumo/legenda — não expõe cursor navegável. Nenhum artefato deve incluí-lo
como condição de existência ou ativação de `[✥]`.

## Consequências

### Artefatos a corrigir em tarefa subsequente

Os arquivos abaixo devem ser atualizados por uma tarefa separada, após aceite desta ADR.
**Esta tarefa (DOC-0010) não altera esses arquivos.**

| Arquivo | Correção necessária |
|---|---|
| `docs/NOMENCLATURA.md` | Seção 5.1: remover `lancador` da condição de existência de `[✥]`; restringir a `dado` |
| `docs/contratos/contrato_composicao_corpo.md` | Seção 5.2: remover "lancador é corpo navegável" (no sentido de `[✥]`) |
| `docs/contratos/contrato_barra_de_menus.md` | Seção 6.3 e critérios de validação: clarificar que "corpo navegável" = corpo tipo `dado` |
| `config/barra_de_menus.json` | Chip `navegar`, campo `existencia`: substituir referência a "dado ou menu" por referência exclusiva a `dado` |

### Arquivos que não devem ser alterados por esta decisão

| Arquivo | Motivo |
|---|---|
| `config/lancador.json` | Campo `navegacao` permanece — descreve mecânica interna do `lancador`, não navegação por `[✥]` |
| `docs/contratos/contrato_lancador.md` | Não declara `[✥]` — não precisa ser corrigido |
| `docs/contratos/contrato_estilo.md` | Não referencia tipos navegáveis |
| `docs/contratos/contrato_cabecalho.md` | Fora do escopo |
| Qualquer arquivo de código | Implementação aguarda contratos corrigidos |
| Qualquer arquivo em `docs/relatorios/` | Não é normativo |

### Impacto na mecânica do `lancador`

O `lancador` continua sendo um objeto válido do corpo, com layout em fila/matriz calculado
automaticamente, estrutura de item `chip + texto + tela_destino`, e mecânica interna própria
registrada em `config/lancador.json`. Nada disso muda. O que muda é a exclusão do `lancador` da
condição de existência e ativação de `[✥]`.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| Manter `lancador` como navegável por `[✥]` com mecânica diferenciada | Criaria dois comportamentos de `[✥]` não especificados; amplia escopo sem caso de uso concreto |
| Renomear `dado` para `console` ao mesmo tempo | Mistura duas decisões distintas; a renomeação não foi decidida e tem escopo próprio |
| Criar novo tipo `navegavel` que englobe `lancador` e `dado` | Introduz abstração não necessária na taxonomia atual; soma complexidade sem benefício imediato |
