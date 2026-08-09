---
name: ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher
description: "Estabelece a presença obrigatória de [ ? ] Ajuda em todas as telas e a representação contextual de Espaço para expandir ou recolher ramos de arvore_colapsavel"
metadata:
  type: adr
  status: aceita_e_aplicada
  id: ADR-0043
  data: "2026-08-08"
  substitui: null
rastreabilidade:
  decisao_usuario: "D-CHIP-01 a D-CHIP-12 — Ajuda universal, permanência e posição canônica, identidade contextual de Espaço em arvore_colapsavel, derivação pelo item corrente, compatibilidade com ADR-0042, seleção múltipla e ADR-0041, reconciliação posterior de H-0053 e fora de escopo da integração demonstrativa multilinha/paginada"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0007
  contratos_afetados:
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
  handoffs_bloqueados:
    - H-0053
  QA_ADR: ADR_APPROVED
  aplicacao_documental: executada
  QA_APLICACAO: ADR_APPLICATION_APPROVED
---

# ADR-0043 — Ajuda universal e chip contextual de expandir/recolher

## 1. Status

`aceita e aplicada`

```yaml
status: aceita_e_aplicada
QA_ADR: ADR_APPROVED
aplicacao_documental: executada
QA_APLICACAO: ADR_APPLICATION_APPROVED
```

Esta ADR registra decisões normativas fechadas. Sua aplicação documental foi
executada nos contratos e módulos de nomenclatura afetados. Ela não substitui
a ADR-0042 nem implementa H-0053. O QA da aplicação documental foi aprovado.

## 2. Contexto

### 2.1 Autoridades lidas

Esta ADR foi redigida com base exclusiva nas seguintes autoridades do
manifesto de leitura desta etapa:

- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`;
- `docs/adr/ADR-0042-navegacao-multinivel-do-console.md`;
- `docs/contratos/contrato_barra_de_menus.md`;
- `docs/contratos/contrato_chip.md`;
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`;
- `docs/nomenclatura/32_CONSOLE.md`;
- `docs/templates/TEMPLATE_ADR.md`.

A ADR-0041 foi consultada somente pela saída focal de `PageUp`, `PageDown`,
`Páginas`, `página` e `pagina`, conforme o manifesto. Sua autoridade de
paginação não é reaberta nesta ADR.

### 2.2 Problema

O estado documental vigente trata `[?] Ajuda` como chip declarativo por tela.
Essa regra é insuficiente para a política universal agora fechada: toda tela
do Orquestrador deve possuir `[?] Ajuda`, sem que a barra deixe de ser
declarativa em sua composição geral.

Também não existe identidade normativa específica para o uso contextual da
tecla física `Espaço` quando ela abre ou fecha ramos em
`politica_navegacao.tipo = arvore_colapsavel`. A mesma tecla já pertence à
semântica de seleção múltipla em outras capacidades. A identidade do chip
precisa, portanto, ser determinada pela função contextual e não somente pela
tecla física.

Esta ADR fecha essas duas lacunas prospectivamente. Não materializa schema,
JSON, identificadores internos adicionais, código ou fixtures.

## 3. Decisões explícitas do usuário

As decisões abaixo são transportadas integralmente. Nenhuma alternativa de
arquitetura, schema, contrato de ação, implementação ou nomenclatura interna
é escolhida além da semântica necessária já fornecida.

### D-CHIP-01 — Ajuda universal

```yaml
chip:
  tecla: "?"
  rotulo: "Ajuda"
representacao: "[?] Ajuda"
existencia: OBRIGATORIA
escopo: TODAS_AS_TELAS
```

Toda tela do Orquestrador deve possuir `[?] Ajuda`. A barra continua
declarativa em sua composição geral, mas Ajuda deixa de ser opcional. Nenhuma
tela pode omiti-la.

### D-CHIP-02 — Permanência de Ajuda

`[?] Ajuda` permanece presente em todos os estados da mesma tela, em todas as
páginas de consoles paginados, após mudança de foco e quando a largura for
insuficiente.

Quando não houver largura suficiente para a barra declarada, aplica-se a regra
vigente de erro de layout. Chips não são omitidos para fazer a barra caber.
A paginação do console não cria nova tela nem nova barra.

### D-CHIP-03 — Posição de Ajuda

Preserva-se integralmente a gramática canônica de ordem vigente em
`docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`,
`docs/contratos/contrato_barra_de_menus.md` e
`docs/contratos/contrato_chip.md`. O chip contextual de `Espaço` ocupa, dentro
dessa gramática, a posição correspondente à faixa já vigente de chips
específicos/contextuais e permanece antes de `[?] Ajuda`, que continua sendo o
último chip. Esta ADR não reproduz uma segunda ordenação, não reordena chips
não relacionados e preserva todas as relações canônicas existentes.

### D-CHIP-04 — Identidade contextual de Espaço

Quando `Espaço` executar expansão ou recolhimento em
`politica_navegacao.tipo = arvore_colapsavel`, a barra apresenta um chip
contextual próprio.

Esse chip usa a tecla física `Espaço` e o símbolo Unicode canônico de espaço
adotado visualmente pela barra, `␣`. Ele não possui semântica de seleção, não é
o chip canônico `[␣] Selecionar` e não reaproveita a semântica, os critérios de
existência ou o estado ativo da seleção múltipla somente porque a tecla física
é a mesma.

A identidade normativa é determinada pela função, não apenas pela tecla.

### D-CHIP-05 — Ramo expandido

Quando o item corrente/focalizável da árvore possui filhos e está expandido,
a barra mostra:

```text
[␣] Recolher
```

Ele permanece presente e ativo. O efeito contextual é inequívoco: pressionar
`Espaço` recolhe o ramo corrente conforme a semântica de `arvore_colapsavel`.

### D-CHIP-06 — Ramo recolhido

Quando o item corrente possui filhos e está recolhido, a barra mostra:

```text
[␣] Expandir
```

Ele permanece presente e ativo. O efeito contextual é inequívoco: pressionar
`Espaço` expande o ramo corrente conforme a semântica de `arvore_colapsavel`.

### D-CHIP-07 — Folha

Quando o item corrente não possui filhos, a barra mantém:

```text
[␣] Expandir
```

porém com:

```yaml
ativo: false
```

Deve ser usada a apresentação canônica vigente de chip inativo, preservada a
capitalização normal do rótulo e inalterada a semântica de `Espaço` sobre a
folha. Pressionar `Espaço` não cria seleção, expansão fictícia ou ação nova.
O estado inativo comunica que não existe capacidade de expansão para aquele
item.

### D-CHIP-08 — Regra contextual

O texto do chip é derivado exclusivamente do item corrente e de seu estado de
expansão, nunca do estado global da árvore.

| Item corrente | Estado | Chip |
|---|---|---|
| ramo com filhos | expandido | `[␣] Recolher` ativo |
| ramo com filhos | recolhido | `[␣] Expandir` ativo |
| folha | não aplicável | `[␣] Expandir` inativo |

Mudança de cursor pode alterar imediatamente o texto e o estado ativo do
chip. Isso é comportamento contextual esperado e não mutação estrutural da
barra.

### D-CHIP-09 — Cursor, foco e origem do estado contextual

O estado contextual é derivado do item corrente do console focalizado. Não é
derivado de:

- seleção;
- primeiro item da árvore;
- último ramo alterado;
- nome da fixture;
- página global;
- item oculto;
- ramo sem cursor.

Para a política `arvore_colapsavel`, a focalização exige cursor capaz de
percorrer os nós e abrir/recolher níveis. A invariável normativa é:

```yaml
arvore_colapsavel:
  quando_focalizado:
    item_corrente_navegavel: OBRIGATORIO

  se_existem_nos_navegaveis_visiveis:
    cursor:
      deve_existir: true
      deve_apontar_para_item_visivel_valido: true

  se_nao_existe_nenhum_no_navegavel_visivel:
    console_focalizavel_nesta_politica: false
```

Não existe estado normativo válido de console `arvore_colapsavel`
focalizado sem item corrente ou cursor; portanto, não há estado do chip
contextual a escolher como fallback. Se não houver nó navegável visível, o
console não é focalizável nesta política.

As transições que exigem reconciliação são:

```yaml
reconciliacao:
  gatilhos_possiveis:
    - troca_de_pagina
    - expansao
    - recolhimento
    - recomputacao_da_projecao_visivel

  requisito:
    cursor_deve_ser_valido_antes_da_interacao_contextual: true
```

A implementação concreta da reconciliação permanece responsabilidade da
infraestrutura vigente. Esta ADR não escolhe política nova de borda, não
redefine paginação nem determina qual item deve ser escolhido quando
autoridades existentes já fecharem isso. Se uma situação futura exigir escolha
adicional realmente não normatizada, ela pertence a decisão própria; não se
cria focalização sem cursor como fallback.

### D-CHIP-10 — Compatibilidade com `arvore_colapsavel`

A ADR não redefine a semântica de navegação da ADR-0042. Continuam valendo:

- `↑`/`↓` percorrem a projeção navegável autorizada;
- `Espaço` abre ou fecha ramo;
- folha não possui ação de expansão;
- não existe seleção;
- não existe `Todos`;
- não há nova semântica de `Enter`;
- não há nova semântica de `←`/`→`.

Esta ADR define somente a representação, na barra de menus, da ação já
existente.

### D-CHIP-11 — Compatibilidade com seleção múltipla

O chip `[␣] Selecionar` continua pertencendo à semântica de seleção nas
capacidades que a utilizam. Os chips `[␣] Expandir` e `[␣] Recolher` pertencem
à expansão e ao recolhimento de árvore.

A mesma tecla física pode possuir chips semanticamente distintos em políticas
distintas. Os contratos funcionais não devem ser fundidos.

### D-CHIP-12 — Paginação

A existência e o estado do chip contextual acompanham o item corrente da
página vigente. A ADR não cria nova paginação.

Preserva-se integralmente:

```text
ADR-0041
PageUp
PageDown
[PgUp][PgDn] Páginas
```

A troca de página pode mudar o item corrente e, consequentemente, mudar
`[␣] Expandir` ou `[␣] Recolher`. `[?] Ajuda` permanece presente
independentemente da página.

## 4. Consequências

### 4.1 Consequências normativas

- `[?] Ajuda` torna-se uma presença universal obrigatória sem converter a
  barra em uma lista global hardcoded de chips.
- O estado e o texto do chip contextual passam a acompanhar o cursor do
  console focalizado, inclusive durante a troca de página.
- A tecla física `Espaço` fica explicitamente desambiguada por função entre
  seleção múltipla e expansão/recolhimento de árvore.
- Chips inativos continuam visíveis e seguem a apresentação canônica vigente;
  a folha não ganha ação implícita.
- A semântica de navegação da ADR-0042 e a autoridade universal de paginação
  da ADR-0041 permanecem intactas.

### 4.2 Custos e restrições

- A aplicação documental atualizou os contratos e módulos de nomenclatura
  proprietários para registrar a obrigatoriedade universal de Ajuda e a
  identidade contextual de `Espaço`.
- Todas as telas existentes deverão convergir documentalmente para a presença
  de `[?] Ajuda`; a materialização concreta dessa convergência pertence à
  aplicação e aos handoffs ou patches apropriados.
- Instâncias de `arvore_colapsavel` deverão convergir para o chip contextual
  definido nesta ADR; a implementação não pode reaproveitar o contrato de
  seleção múltipla apenas por compartilhar a tecla física.
- Nenhum schema concreto, campo JSON adicional, identificador interno além
  da semântica das decisões, código ou fixture é criado nesta etapa.

## 5. Compatibilidade e transição

### 5.1 Supersessão parcial

Esta ADR supersede somente a parte das autoridades anteriores que permitia
omitir `[?] Ajuda` ou tratava sua presença como opcional por tela.

Em particular, ficam parcialmente supersedidas as formulações de
`ADR-0012`, do `contrato_barra_de_menus.md`, do `contrato_chip.md` e de
`31_BARRA_DE_MENUS_E_CHIPS.md` que afirmavam que `[?]` podia estar ausente ou
que a existência de um chip canônico não obrigava sua presença em toda tela.
Essa supersessão é restrita a `[?] Ajuda`; não torna obrigatórios os demais
chips condicionais nem altera a composição declarativa geral.

### 5.2 Regras preservadas

1. A composição geral da barra continua declarativa por tela.
2. Chips já declarados continuam seguindo suas regras vigentes de existência,
   ativo/inativo, posição e ação, salvo a regra nova e específica de Ajuda e
   de `Espaço` em `arvore_colapsavel`.
3. Todas as telas deverão convergir para a presença de `[?] Ajuda`.
4. `arvore_colapsavel` deverá convergir para o chip contextual
   `[␣] Expandir`/`[␣] Recolher` conforme o item corrente.
5. A aplicação documental atualizou os contratos e a nomenclatura proprietários
   afetados.
6. A implementação e a configuração concreta ocorrerão em handoffs ou
   patches de implementação apropriados.

### 5.3 Precedência em relação à ADR-0042

A ADR-0042 continua sendo a autoridade da navegação multinível e da
semântica de `arvore_colapsavel`. Esta ADR apenas especializa sua
representação na barra de menus para a ação de `Espaço`. Não altera percurso,
seleção, entrada por setas, `Enter`, `←`/`→` ou qualquer outra regra da
ADR-0042.

### 5.4 Precedência em relação à ADR-0041

A ADR-0041 continua sendo a autoridade universal de paginação. A mudança de
página acompanha a regra vigente e pode alterar o item corrente e o chip
contextual; não há novo comando nem nova notação de paginação.

## 6. Documentos atualizados na aplicação

A aplicação documental atualizou, sem antecipar implementação, os seguintes
documentos proprietários:

| Documento | Atualização necessária |
|---|---|
| `docs/contratos/contrato_barra_de_menus.md` | Registrar Ajuda obrigatória em todas as telas, sua permanência e posição final, a inserção do chip contextual antes de Ajuda e a distinção funcional de `Espaço`. |
| `docs/contratos/contrato_chip.md` | Registrar a identidade contextual de `[␣] Expandir`/`[␣] Recolher`, a derivação pelo item corrente, o estado inativo de folha e a separação de `[␣] Selecionar`, sem inventar schema novo. |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Atualizar a terminologia de Ajuda universal, a ordem aplicável e a identidade dos chips contextuais da árvore. |
| `docs/nomenclatura/32_CONSOLE.md` | Registrar a relação entre item corrente, console focalizado e chip contextual de `arvore_colapsavel`, preservando cursor, foco, seleção e paginação como mecanismos distintos. |

Os documentos acima foram alterados nesta aplicação. Nenhum schema concreto,
identificador interno não decidido, código ou fixture foi criado.

## 7. Impactos conhecidos em H-0053

As consequências para H-0053 são registradas, não implementadas.

H-0053 foi reconciliado após a aplicação da ADR-0043, com implementação e
validação manual aprovadas:

```yaml
H-0053:
  handoff: concluido
  fixture: implementada
  implementacao: IMPLEMENTED
  validacao_manual: MANUAL_VALIDATION_APPROVED
```

A implementação futura da fixture H-0053 deverá também usar a hierarquia
demonstrativa:

```text
1.
1.1
1.2
1.2.1
2.
2.1
```

em substituição ao antigo item `a)`. Essa mudança é demonstrativa, não uma
regra normativa universal de identificação de nós.

Os itens da fixture deverão possuir texto suficiente para que alguns nós
ocupem mais de uma linha, tornando a demonstração futura mais representativa.
Rótulos e comprimentos não se tornam requisitos gerais da árvore.

## 8. Fora de escopo

Ficam fora do escopo desta ADR:

- QA da ADR;
- alteração de contratos funcionais, schema ou nomenclatura interna não
  decidida;
- patch do H-0053;
- código, configuração concreta, fixtures e handoffs;
- criação ou alteração de backlog;
- paginação futura ou nova semântica de paginação;
- validação manual e fechamento;
- integração demonstrativa/visual dedicada entre:
  - `arvore_colapsavel`;
  - itens de múltiplas linhas;
  - paginação;
  - mudança de página;
  - preservação de cursor;
  - expansão/recolhimento atravessando cenários paginados.

Depois do H-0053, o gerente deverá verificar o backlog vigente para saber se
essa integração já possui item ou ciclo proprietário. Somente se não existir
item adequado deverá ser criado novo ITEM. Não se deve presumir que ITEM-0024
cubra essa integração apenas por tratar geometria multinível.

## 9. Critérios para aplicação

- [ ] A aplicação supersede somente a permissão de omitir `[?] Ajuda`; a
      composição geral da barra continua declarativa.
- [ ] Todas as telas convergem para `[?] Ajuda`, que permanece nas páginas,
      estados, focos e situações de largura insuficiente; erro de layout não
      autoriza omissão.
- [ ] `[?] Ajuda` permanece como último chip, e o chip contextual de `Espaço`
      ocupa a faixa de específicos/contextuais da gramática vigente e permanece
      antes dele, sem redefinir a ordenação completa dos demais.
- [ ] `arvore_colapsavel` apresenta `[␣] Recolher` para ramo corrente
      expandido, `[␣] Expandir` para ramo corrente recolhido e `[␣] Expandir`
      inativo para folha.
- [ ] O texto e o estado são derivados exclusivamente do item corrente do
      console focalizado, e não de seleção, página global, fixture ou estado
      global da árvore.
- [ ] `[␣] Selecionar` e os chips contextuais de expansão/recolhimento não
      compartilham contrato funcional apenas por usarem a tecla `Espaço`.
- [ ] A aplicação não cria ação fictícia para folha nem seleção em
      `arvore_colapsavel`.
- [ ] A semântica de navegação da ADR-0042 e a paginação da ADR-0041 são
      preservadas integralmente.
- [ ] H-0053 é reconciliado antes da retomada da validação manual, com a
      hierarquia e os textos demonstrativos registrados nesta ADR.
- [ ] Não há implementação de código, alteração de fixture ou criação de
      ITEM nesta aplicação documental sem decisão e etapa próprias.

## 10. Critérios de aceite documental

- [ ] A ADR identifica o problema das duas lacunas normativas.
- [ ] D-CHIP-01 a D-CHIP-12 estão registrados sem alternativa escolhida.
- [ ] A relação de precedência com ADR-0012, ADR-0042 e ADR-0041 está
      explicitamente delimitada.
- [ ] A supersessão de autoridades anteriores é parcial e restrita à omissão
      de `[?] Ajuda`.
- [ ] A identidade contextual de `Espaço` está separada da seleção múltipla.
- [ ] Os impactos conhecidos em H-0053 e a demonstração hierárquica estão
      registrados como consequências, não como implementação.
- [ ] A integração demonstrativa multilinha/paginada está registrada como
      fora de escopo e não cria ITEM de backlog nesta ADR.
- [ ] Nenhum schema concreto ou identificador interno não decidido é
      inventado.

## 11. Alternativas consideradas

Não há alternativas a escolher nesta ADR. As decisões normativas foram
fechadas diretamente pelo usuário e são registradas sem seleção, desenho
adicional ou reabertura.

## 12. Bloqueios

nenhum
