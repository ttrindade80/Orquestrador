---
name: ADR-0002-menu-sobra-direita
description: Corpo tipo menu deixa de centralizar o bloco e passa a acumular sobra à direita
metadata:
  type: adr
  status: aceita
  data: 2026-07-05
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_composicao_corpo.md
  handoffs_bloqueados: []
---

# ADR-0002 — `menu` usa sobra à direita

## Status

`aceita`

## Contexto

A seção 5.2 de `contrato_composicao_corpo.md` especificava que o bloco do
corpo tipo `menu` era centralizado horizontalmente no espaço disponível —
a sobra de espaço se distribuía igualmente dos dois lados do bloco.

Decisão fechada em sessão de 2026-07-05 (`docs/NOMENCLATURA.md` seção 8.1):
o alinhamento passa a ser à esquerda do espaço disponível, com toda a sobra
de espaço ficando à direita do bloco. A regra vale tanto para modo `fila`
quanto para modo `matriz`.

A decisão não afeta corpo tipo `dado`, cujas regras de alinhamento permanecem
inalteradas. O objeto `Info` permanece fora do escopo desta ADR — seu
alinhamento será tratado em decisão específica (DOC-B004).

## Decisão

O bloco do corpo tipo `menu` é posicionado à esquerda do espaço horizontal
disponível. A sobra de espaço, após aplicar as regras de largura e vãos
vigentes, fica inteiramente à direita do bloco.

Esta regra substitui a centralização anterior e vale para os dois modos de
layout:

| Modo | Comportamento anterior | Comportamento após ADR-0002 |
|---|---|---|
| `fila` | Bloco centralizado (sobra dividida dos dois lados) | Bloco à esquerda (sobra à direita) |
| `matriz` | Bloco centralizado (sobra dividida dos dois lados) | Bloco à esquerda (sobra à direita) |

O alinhamento interno dos itens dentro do bloco não muda: todos os chips `[`
permanecem na mesma posição horizontal entre si (alinhados à esquerda dentro
do bloco).

## Consequências

- Menu passa a ser ancorado à margem esquerda do espaço disponível; o espaço
  em branco acumula à direita.
- Corpo tipo `dado` não é afetado por esta decisão.
- Objeto `Info` permanece fora de escopo — aguarda decisão específica (DOC-B004).
- Esta ADR não introduz nem altera vãos elásticos — esse é escopo da ADR-0003.
- `contrato_composicao_corpo.md` seção 5.2 (alinhamento horizontal) e o
  critério de validação correspondente na seção 7 são atualizados junto com
  esta ADR.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Manter centralização | Contraria a decisão fechada em sessão de 2026-07-05 |
| Sobra à esquerda (bloco à direita) | Não foi esta a decisão — a sobra fica à direita, não à esquerda |
| Aplicar mesma regra ao `Info` | `Info` está fora de escopo — aguarda decisão específica (DOC-B004) |
| Aplicar mesma regra ao `dado` | `dado` não foi objeto desta decisão e permanece com suas regras atuais |
