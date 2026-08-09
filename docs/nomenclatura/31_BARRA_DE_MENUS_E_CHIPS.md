---
name: nomenclatura-barra-de-menus-e-chips
description: Terminologia da barra_de_menus e chips — região fixa inferior da tela, chips canônicos e específicos, estados, distribuição, indicadores e comandos visuais da barra
metadata:
  type: nomenclatura
  scope: barra_de_menus_e_chips
  fase_de_aplicacao: VIGENTE
---

# Barra de menus e chips

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário dos termos de:
- `barra_de_menus` como região e instância declarada;
- chip como entidade declarativa de interface (definição de tipo);
- chip canônico e chip específico;
- estado ativo e inativo de chip;
- distribuição visual da barra;
- indicadores e comandos visuais da barra;
- chips `[Esc]`, `[✥]`, `[V]`, `[⏎]`, `[PgUp][PgDn]`, `[-][+]`, `[#]`, `[⇆]`, `[␣]`, `[?]` enquanto termos de interface.

Comportamento completo de cada comando permanece nos contratos
`contrato_barra_de_menus.md` e `contrato_chip.md`.

## 3. Termos proprietários

- `barra_de_menus` (como região e instância)
- chip (entidade declarativa)
- chip canônico
- chip específico
- estado ativo / estado inativo
- `barra_de_menus.distribuicao`
- `barra_de_menus.distribuicao = "horizontal"` (alias transitório)
- `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` (forma canônica futura)
- ordem fixa dos chips canônicos
- tipos de chip específico: toggle, múltiplo, aciona processo, aciona tela
- rótulo dinâmico (`[⏎]` e `[Esc]`)
- `[Ins] Dry-Run` (chip específico do fluxo focal; ADR-0037)
- controle universal de execução real e `dry-run` (chip específico reutilizável; ADR-0040)
- declaração `controle_execucao` e `controle_execucao.modo_inicial` do controle universal (ADR-0040)
- ativo destacado (via `cor_alerta`; ADR-0037)
- paginação limitada de `[PgUp][PgDn]` (ADR-0038; tecla e notação especializadas pela ADR-0041)
- teclas universais de paginação `PageUp`/`PageDown` (ADR-0041)
- representação canônica `[PgUp][PgDn] Páginas` (ADR-0041)
- Ajuda universal (`[?] Ajuda`) e chip contextual de árvore (`[␣] Expandir` /
  `[␣] Recolher`) (ADR-0043)

## 4. Definições

### 4.1 `barra_de_menus` como região

`barra_de_menus` é a região fixa inferior de toda tela do sistema. Ela é
uma instância declarada pela tela no JSON. A barra é espelho da declaração —
nunca fonte de decisão sobre composição.

**Declarativa por tela (ADR-0012, especializada pela ADR-0043)**: a
`barra_de_menus` continua declarativa para os demais chips. `[?] Ajuda` é
universal e obrigatório em toda tela; os demais chips seguem suas condições
de existência declaradas.

### 4.2 Chip

Chip é uma entidade declarativa de interface textual. Representa uma tecla
ou símbolo acionável — ou informativo — exibido na região da tela.

| Categoria | Definição |
|---|---|
| chip canônico | Chip pertencente à ordem fixa definida pelo sistema; `[?] Ajuda` é universal e obrigatório, enquanto os demais seguem sua condição declarada |
| chip específico | Chip próprio da classe de tela; posicionado entre `[⏎]` e `[V]/[?]` na ordem |

### 4.3 Ordem fixa dos chips canônicos

```
[Esc] → [PgUp][PgDn] → [-][+] → [#] → [⇆] → [✥] → [␣] → [⏎] → específicos → [V] → [?]
```

| Chip | Rótulo | Condição de existência |
|---|---|---|
| `[Esc]` | Sair / Voltar / Limpar | declarativa por tela |
| `[PgUp][PgDn]` | Páginas | classe declara `paginacao: com`; topologia limitada, sem wrap entre primeira e última página (ADR-0038); tecla e representação canônica fixadas pela ADR-0041 |
| `[-][+]` | Colunas | classe declara `colunas_ajustavel: com` (tipo `console`) |
| `[#]` | Grupos | classe declara filtro por grupo |
| `[⇆]` | Alternar | tela possui pelo menos dois consoles focalizáveis (ADR-0031 D14) |
| `[✥]` | Navegar | console focado possui mais de um item navegável na página atual (ADR-0031 D14; universo restrito à página atual pela ADR-0038); existência dinâmica — ausente quando a condição não é satisfeita |
| `[␣]` | Selecionar | classe declara formação de seleção |
| `[⏎]` | Todos / Executar / Visualizar | declarativa por tela |
| específicos | (por classe) | chips próprios da classe |
| `[V]` | Verboso | política de modo `alternavel` (ADR-0028) |
| `[?]` | Ajuda | obrigatória em toda tela; sempre ativa e última |

Para `politica_navegacao.tipo = arvore_colapsavel`, o chip contextual de
Espaço pertence à faixa de específicos/contextuais, depois de `[⏎]` quando
aplicável e antes de `[V]` e `[?]`. Sua representação deriva do item corrente:

| Item corrente | Estado | Representação |
|---|---|---|
| ramo com filhos | expandido | `[␣] Recolher` ativo |
| ramo com filhos | recolhido | `[␣] Expandir` ativo |
| folha | não aplicável | `[␣] Expandir` inativo |

`[␣] Expandir` e `[␣] Recolher` são distintos de `[␣] Selecionar` por
semântica, não por uma nova tecla física ou sinônimo técnico.

### 4.4 Estado ativo e inativo

- **Existência** = propriedade estática declarada pela classe (para a maioria dos chips).
- **Ativo/inativo** = estado dinâmico recalculado a cada render; indicado por
  `cor_inativo` (definida no módulo `10`).
- **Ativo destacado** (ADR-0037) = chip operável cujo texto usa `cor_alerta`
  sem usar `cor_inativo`; destaque não altera a condição de ativo.

O chip continua ocupando sua posição/ordem quando inativo — não desaparece,
só muda de cor e para de reagir ao acionamento.

**Exceção para `[✥]` (ADR-0031 D14)**: `[✥]` possui **existência dinâmica** —
aparece somente quando o console focado possui mais de um item navegável; está
**ausente** (não inativo) quando a condição não é satisfeita. Não assume estado
inativo: ou está presente e ativo, ou está ausente. Ver `contrato_chip.md` §8.

### 4.4.1 Chip específico `[Ins] Dry-Run` (ADR-0037)

Chip específico da tela integrada do Handoff 4 — não é chip canônico
universal. Tipo `alternancia`: toggle focal entre execução real e `dry-run`.
Permanece ativo nos dois estados; ligado usa amarelo via `cor_alerta`; único
eco é a cor do próprio texto. O `ITEM-0020` continua aberto para a futura
implementação e reconciliação dessa escolha com o padrão universal.

### 4.4.2 Paginação limitada de `[PgUp][PgDn]` (ADR-0038; especializada pela ADR-0041)

`[PgUp][PgDn]` são chips canônicos de tipo `navegacao` (existência
declarativa via `paginacao: com`), representação canônica fixada pela
ADR-0041 em substituição a `[<][>]`. A topologia entre páginas é limitada,
não circular: `[PgUp]` inativo na primeira página; `[PgDn]` inativo na
última; ambos inativos com uma única página (`página 1/1`), inclusive com
conjunto vazio de itens visíveis. O estado ativo/inativo é avaliado
exclusivamente pela página do console focado — sem console focado, ou com o
console focado sem paginação declarada, ambos ficam inativos; o acionamento
não altera a página de outro console nem o foco corrente. Entrada aceita:
`PageUp` para página anterior; `PageDown` para próxima página (ADR-0041
D-PGU-01, D-PGU-02); os caracteres `,`, `<`, `.` e `>` deixam de ter
qualquer função de paginação — não são alias, atalho nem fallback (ADR-0041
D-PGU-04). `[✥]` passa a considerar somente os itens navegáveis da página
atual do console focado (ver §4.3).

### 4.4.3 Controle universal de execução real e `dry-run` (ADR-0040)

O **controle universal de execução real e `dry-run`** é um chip específico
padronizado e reutilizável, fora da lista de chips canônicos. Sua existência
está vinculada à declaração válida do objeto raiz `controle_execucao` no
`tela.json`, com `controle_execucao.modo_inicial` obrigatório em `executar` ou
`dry_run` e compatibilidade integral das ações de processo relevantes com os
dois modos. A ausência do objeto ou uma declaração inválida significa ausência
do chip. Usa `Insert` e tem rótulo dinâmico `[Ins] Real` ou `[Ins] Simulação`
(D-DRY-12, rótulos vigentes que substituem `[Ins] Executar`/`[Ins] Dry-Run`,
originalmente fixados por D-DRY-02 — histórico substituído). Permanece ativo
nos dois estados; em `Real` usa aparência ativa normal e, somente em
`Simulação`, o texto usa `cor_alerta`. O rótulo indica o modo corrente da
futura execução — distinto do chip de ação `[⏎] Executar`, que inicia o
processamento do lote atual. O rótulo é a indicação primária e a cor é
reforço.

O termo designa o padrão aplicável por instância de tela. Não é sinônimo do
`[Ins] Dry-Run` focal da ADR-0037, que continua sendo a especialização do
Handoff 4 do `ITEM-0006` e não é migrada por esta aplicação.
O rótulo dinâmico representa o modo corrente preservado na mesma instância;
o ciclo de vida desse modo — inclusive a preservação sob suspensão e a
reinicialização em nova abertura ou recarga — é responsabilidade da tela e do
runtime, não do chip.

### 4.5 Rótulo dinâmico — `[⏎]` e `[Esc]`

Terceiro tipo de propriedade dinâmica, além de existência e ativo/inativo:
rótulo que muda conforme o estado atual.

**`[⏎]` — três estados possíveis:**

| Estado | Rótulo |
|---|---|
| Nada selecionado ainda, tela com seleção/execução | `Todos` |
| Alguma seleção marcada | `Executar` |
| Tela de visualização, sem execução | `Visualizar` |

**`[Esc]`:** se há seleção ativa → `Limpar`; sem seleção → `Sair`/`Voltar`.

### 4.6 Tipos de chip específico

| Tipo | Natureza |
|---|---|
| Toggle | filtro de exibição, liga/desliga |
| Múltiplo | filtro de exibição, conjunto de opções, tipicamente mutuamente exclusivas |
| Aciona processo | executa lógica sobre seleção/lote; estrutura formal pendente |
| Aciona tela | abre outra tela (navegação) |

### 4.7 Distribuição visual da barra (ADR-0014)

| Termo específico completo | Conceito |
|---|---|
| `barra_de_menus.distribuicao = "horizontal"` | Distribuição horizontal responsiva dos chips (alias transitório de `horizontal_responsiva`) |
| `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` | Forma canônica futura da distribuição responsiva dos chips |

**Disambiguação obrigatória — três termos distintos e independentes:**

| Termo específico completo | Região |
|---|---|
| `corpo.arranjo = "horizontal"` | corpo |
| `barra_de_menus.distribuicao = "horizontal"` | barra_de_menus (alias transitório) |
| `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` | barra_de_menus (canônico futuro) |

Esses termos não colapsam: uma substring (`horizontal`) não os identifica
unicamente.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `barra_de_menus` × `lancador` | Barra: região fixa inferior da tela; lancador: elemento do corpo para navegação |
| chip canônico × chip específico | Canônico: ordem fixa do sistema; específico: próprio da classe de tela |
| existência × ativo/inativo | Existência: estática, declarada; ativo/inativo: dinâmico, recalculado |
| ativo × ativo destacado | Ativo: operável; ativo destacado: operável com `cor_alerta` — não é inativo (ADR-0037) |
| `[Ins] Dry-Run` focal × controle universal real/`dry-run` | A especialização focal da ADR-0037 permanece vinculada ao Handoff 4; o controle universal da ADR-0040 é reutilizável por instância de tela e não migra a especialização |
| `[⇆]` × `[✥]` | `[⇆]` muda o foco entre consoles focalizáveis; `[✥]` move o cursor entre itens do console focado |
| `barra_de_menus.distribuicao = "horizontal"` × `corpo.arranjo = "horizontal"` | São termos diferentes em regiões diferentes — não colapsam |
| paginação limitada (entre páginas) × navegação toroidal por eixo (dentro da página) | `[PgUp][PgDn]` não fazem wrap entre primeira e última página (ADR-0038); o toróide por eixo (ADR-0031) só se aplica ao cursor dentro de uma mesma página |

## 6. Relação com contratos

- `contrato_barra_de_menus.md`: autoridade do comportamento normativo completo.
- `contrato_chip.md`: autoridade do comportamento normativo do chip.

## 7. Relação com ADRs

- ADR-0012: `barra_de_menus` declarativa por tela.
- ADR-0014: distribuição horizontal responsiva; regra de alteração por termo específico.
- ADR-0022: barra mínima real (`Esc`, `?`, acesso a estilos).
- ADR-0028: chip `[V] Verboso`; relação com política de modo.
- ADR-0031: condições de existência de `[⇆]` (≥2 consoles focalizáveis) e `[✥]` (console focado com >1 item navegável); existência dinâmica de `[✥]`.
- ADR-0034: fecha, para `politica_selecao: multipla` (`ITEM-0006`), a condição de existência do chip `[␣]` e do rótulo dinâmico `Todos`/`Executar` de `[⏎]` já genéricos neste módulo (§4.3, §4.5); na tela padrão de resultado, `[Esc]` é o único chip declarado, com rótulo fixo `Voltar` (sem seleção ativa nessa tela).
- ADR-0037: chip específico `[Ins] Dry-Run`; distinção ativo/inativo/ativo destacado; supersessão pontual da proibição de chip de `dry-run` (D-SEL-19); `ITEM-0020` permanece aberto para padronização genérica.
- ADR-0040: controle universal de execução real e `dry-run`, distinto da especialização focal da ADR-0037.
- ADR-0038: fecha, para `[PgUp][PgDn]`, a topologia limitada e a avaliação pelo console focado; especializa, para `[✥]`, o universo de avaliação restrito à página atual do console focado.
- ADR-0041: especializa, para toda paginação comum do Orquestrador, a tecla de acionamento (`PageUp`/`PageDown`) e a representação canônica (`[PgUp][PgDn] Páginas`), substituindo `,`/`<`/`.`/`>` e `[<][>]` em todos os documentos normativos; nenhuma outra decisão D-PAG-01 a D-PAG-13 é reaberta.
- ADR-0043: torna `[?] Ajuda` universal, sempre ativa e última; distingue
  `[␣] Expandir`/`[␣] Recolher` de `[␣] Selecionar` e os posiciona na faixa de
  específicos/contextuais para `arvore_colapsavel`.

## 8. Aliases ou termos descontinuados relacionados

- `barra_de_menus.distribuicao = "horizontal"` → alias transitório de
  `horizontal_responsiva` (ADR-0014). Ver módulo `90`.
- Formas transitórias da distribuição da barra → módulo `90`.

## 9. Conteúdo que não pertence a este módulo

- Aparência visual do chip (campos de estilo) → módulo `10`.
- Alternância de modo verboso (comportamento completo) → `contrato_barra_de_menus.md`.
- Tipos de apresentações multinível → módulo `44`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§5 (linhas 532-682)"
  intervalo_ou_bloco: "NOM-LEV-011"
origem_normativa: ADR-0012, ADR-0014, ADR-0022, ADR-0028, ADR-0031
contratos_relacionados:
  - contrato_barra_de_menus.md
  - contrato_chip.md
adrs_relacionadas:
  - ADR-0012
  - ADR-0014
  - ADR-0022
  - ADR-0028
  - ADR-0031
  - ADR-0038
  - ADR-0041
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
