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
| `[<][>]` | Páginas | classe declara `paginacao: com` |
| `[-][+]` | Colunas | classe declara `colunas_ajustavel: com` (tipo `console`) |
| `[#]` | Grupos | classe declara filtro por grupo |
| `[⇆]` | Alternar | `quantidade_corpos: multiplos` |
| `[✥]` | Navegar | tela possui ao menos um corpo tipo `console` navegável |
| `[␣]` | Selecionar | classe declara formação de seleção |
| `[⏎]` | Todos / Executar / Visualizar | declarativa por tela |
| específicos | (por classe) | chips próprios da classe |
| `[V]` | Verboso | política de modo `alternavel` (ADR-0028) |
| `[?]` | Ajuda | declarativa por tela |

### 4.4 Estado ativo e inativo

- **Existência** = propriedade estática declarada pela classe.
- **Ativo/inativo** = estado dinâmico recalculado a cada render; indicado por
  `cor_inativo` (definida no módulo `10`).

O chip continua ocupando sua posição/ordem quando inativo — não desaparece,
só muda de cor e para de reagir ao acionamento.

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
| `[⇆]` × `[✥]` | `[⇆]` muda foco entre corpos; `[✥]` move cursor dentro do corpo em foco |
| `barra_de_menus.distribuicao = "horizontal"` × `corpo.arranjo = "horizontal"` | São termos diferentes em regiões diferentes — não colapsam |

## 6. Relação com contratos

- `contrato_barra_de_menus.md`: autoridade do comportamento normativo completo.
- `contrato_chip.md`: autoridade do comportamento normativo do chip.

## 7. Relação com ADRs

- ADR-0012: `barra_de_menus` declarativa por tela.
- ADR-0014: distribuição horizontal responsiva; regra de alteração por termo específico.
- ADR-0022: barra mínima real (`Esc`, `?`, acesso a estilos).
- ADR-0028: chip `[V] Verboso`; relação com política de modo.

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
origem_normativa: ADR-0012, ADR-0014, ADR-0022, ADR-0028
contratos_relacionados:
  - contrato_barra_de_menus.md
  - contrato_chip.md
adrs_relacionadas:
  - ADR-0012
  - ADR-0014
  - ADR-0022
  - ADR-0028
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
