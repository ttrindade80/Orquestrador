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
- chips `[Esc]`, `[✥]`, `[V]`, `[⏎]`, `[<][>]`, `[-][+]`, `[#]`, `[⇆]`, `[␣]`, `[?]` enquanto termos de interface.

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
- ativo destacado (via `cor_alerta`; ADR-0037)
- paginação limitada de `[<][>]` (ADR-0038)
- entradas aceitas de página anterior/próxima página (ADR-0038)

## 4. Definições

### 4.1 `barra_de_menus` como região

`barra_de_menus` é a região fixa inferior de toda tela do sistema. Ela é
uma instância declarada pela tela no JSON. A barra é espelho da declaração —
nunca fonte de decisão sobre composição.

**Declarativa por tela (ADR-0012)**: a `barra_de_menus` não contém todos
os chips canônicos por padrão. Cada tela declara apenas os chips aplicáveis.

### 4.2 Chip

Chip é uma entidade declarativa de interface textual. Representa uma tecla
ou símbolo acionável — ou informativo — exibido na região da tela.

| Categoria | Definição |
|---|---|
| chip canônico | Chip pertencente à ordem fixa definida pelo sistema; sua existência é condicional à composição declarada pela tela |
| chip específico | Chip próprio da classe de tela; posicionado entre `[␣]` e `[V]/[?]` na ordem |

### 4.3 Ordem fixa dos chips canônicos

```
[Esc] → [<][>] → [-][+] → [#] → [⇆] → [✥] → [␣] → [⏎] → específicos → [V] → [?]
```

| Chip | Rótulo | Condição de existência |
|---|---|---|
| `[Esc]` | Sair / Voltar / Limpar | declarativa por tela |
| `[<][>]` | Páginas | classe declara `paginacao: com`; topologia limitada, sem wrap entre primeira e última página (ADR-0038) |
| `[-][+]` | Colunas | classe declara `colunas_ajustavel: com` (tipo `console`) |
| `[#]` | Grupos | classe declara filtro por grupo |
| `[⇆]` | Alternar | tela possui pelo menos dois consoles focalizáveis (ADR-0031 D14) |
| `[✥]` | Navegar | console focado possui mais de um item navegável na página atual (ADR-0031 D14; universo restrito à página atual pela ADR-0038); existência dinâmica — ausente quando a condição não é satisfeita |
| `[␣]` | Selecionar | classe declara formação de seleção |
| `[⏎]` | Todos / Executar / Visualizar | declarativa por tela |
| específicos | (por classe) | chips próprios da classe |
| `[V]` | Verboso | política de modo `alternavel` (ADR-0028) |
| `[?]` | Ajuda | declarativa por tela |

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
eco é a cor do próprio texto. O `ITEM-0020` continua responsável pela futura
padronização genérica dessa escolha.

### 4.4.2 Paginação limitada de `[<][>]` (ADR-0038)

`[<][>]` são chips canônicos de tipo `navegacao` (existência declarativa via
`paginacao: com`). A topologia entre páginas é limitada, não circular: `[<]`
inativo na primeira página; `[>]` inativo na última; ambos inativos com uma
única página (`página 1/1`), inclusive com conjunto vazio de itens visíveis.
O estado ativo/inativo é avaliado exclusivamente pela página do console
focado — sem console focado, ou com o console focado sem paginação
declarada, ambos ficam inativos; o acionamento não altera a página de outro
console nem o foco corrente. Entradas aceitas: `,`/`<` para página anterior;
`.`/`>` para próxima página. `[✥]` passa a considerar somente os itens
navegáveis da página atual do console focado (ver §4.3).

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
| `[Ins] Dry-Run` × padrão universal real/`dry-run` | Especialização focal do Handoff 4; padronização genérica permanece no `ITEM-0020` |
| `[⇆]` × `[✥]` | `[⇆]` muda o foco entre consoles focalizáveis; `[✥]` move o cursor entre itens do console focado |
| `barra_de_menus.distribuicao = "horizontal"` × `corpo.arranjo = "horizontal"` | São termos diferentes em regiões diferentes — não colapsam |
| paginação limitada (entre páginas) × navegação toroidal por eixo (dentro da página) | `[<][>]` não fazem wrap entre primeira e última página (ADR-0038); o toróide por eixo (ADR-0031) só se aplica ao cursor dentro de uma mesma página |

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
- ADR-0038: fecha, para `[<][>]`, a topologia limitada, a avaliação pelo console focado e as entradas aceitas; especializa, para `[✥]`, o universo de avaliação restrito à página atual do console focado.

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
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
