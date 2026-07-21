---
name: nomenclatura-console
description: Terminologia do console — container interativo e navegável, cursor, seleção, lote, grupo como origem do dado, partes do item (ec/tg/tx), navegação
metadata:
  type: nomenclatura
  scope: console
  fase_de_aplicacao: VIGENTE
---

# Console

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
- console como container interativo e navegável;
- cursor (selecionado);
- seleção como conjunto nomeado;
- lote como unidade de execução;
- grupo quando usado como categoria ou origem do dado (sentido do dado);
- item do console e suas partes `ec`, `tg`, `tx`;
- navegação do console enquanto vocabulário;
- relações conceituais com barra e conteúdo externo.

Não redefinir `grupo` como nó estrutural; esse sentido pertence ao módulo `40`.

## 3. Termos proprietários

- `console` (identificação e tipo)
- cursor / `selecionado` (como mecanismo de navegação)
- `grupo` (como origem/categoria do dado)
- seleção (conjunto nomeado de elementos)
- lote (unidade de execução)
- `ec` (espaço do cursor)
- `tg` (espaço de toggle)
- `tx` (texto do item)
- item de console
- `[✥]` (enquanto dica visual de navegação)
- wrap toroidal
- paginação é independente da navegação

## 4. Definições

### 4.1 Console como container

`console` é um container interativo e navegável genérico. Pode conter itens
heterogêneos. O cursor navega por itens, não por linhas físicas. Não é
sinônimo de tela, não é `lancador`, não é `dashboard`, não é `barra_de_menus`.

### 4.2 Mecanismos de seleção (quatro conceitos distintos)

| Conceito | O que é | Como se forma |
|---|---|---|
| **Cursor / selecionado** | Aponta um item; `[⏎]` executa ação sobre ele | Navegação via `[✥]` (setas do teclado), indicador `→` |
| **Grupo** | Origem/categoria do dado (ex.: grupo 1, 2, 3) — atributo do próprio dado | Já existe nos dados, filtra exibição via `[#]` |
| **Seleção** | Conjunto nomeado de elementos — cruza grupos livremente, sem limite | Toggle via `[␣]`, indicador `●`/`○`, persiste com nome |
| **Lote** | Unidade de execução — calculado a partir de uma seleção no momento de rodar um processo específico, tipicamente `seleção − o que já foi processado` | Derivado, não é marcado manualmente |

**Lote não é sinônimo de grupo nem de seleção**:
- Grupo: origem/escopo de exibição.
- Seleção: conjunto nomeado que cruza grupos.
- Lote: resultado calculado por processo a partir de uma seleção.

### 4.3 Navegação por `[✥]`

`[✥]` é a dica visual de "use as setas do teclado". A navegação em si é feita
pelas quatro setas.

**Escopo**: `[✥]` e as setas da `barra_de_menus` controlam somente cursor de
corpo tipo `console`. `lancador` não é corpo navegável por `[✥]`. `dashboard`
não é corpo navegável por `[✥]` (ADR-0005).

**Wrap toroidal**: a grade fecha nos dois eixos, cada um independente.
Célula vazia forma seu próprio toróide menor. O cursor nunca entra em célula
vazia.

**Paginação é independente da navegação**: o cursor nunca troca de página
sozinho ao cruzar a borda do toróide. Cada página é seu próprio toróide
fechado.

### 4.4 Estrutura do item do console

Todo item de um corpo tipo `console` navegável tem exatamente três partes,
sempre na mesma ordem:

| Parte | Sigla | Função |
|---|---|---|
| Espaço do cursor | `ec` | onde `selecionado` (`→` ou preset equivalente) aparece quando o cursor está na linha |
| Espaço de toggle | `tg` | onde `incluido` (`●`/`○` ou preset equivalente) aparece |
| Texto do item | `tx` | conteúdo, tamanho variável |

**Uma estrutura só, não duas**: a diferença entre item com seleção real e item
navegável sem seleção é o **conteúdo visual de `tg`** que muda — não a estrutura.

- Com seleção real: `tg` mostra par on/off completo.
- Sem seleção: `tg` mostra símbolo estático (não alterna), configurável via schema.

**Sobreposição `ec` × `tg`**: os dois espaços coexistem em posições distintas
e adjacentes, não se sobrepõem entre si.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `grupo` (sentido do dado) × `grupo` (nó estrutural) | Grupo como origem/categoria do dado pertence ao domínio do console; grupo como nó estrutural do corpo pertence ao módulo `40` — requerem contexto para desambiguação |
| seleção × lote | Seleção: conjunto nomeado persistente; lote: calculado por processo específico no momento de execução |
| cursor × seleção | Cursor aponta um item; seleção é conjunto de itens marcados — são mecanismos independentes |
| `[✥]` (console) × `[⇆]` (barra) | `[✥]` move cursor dentro do corpo em foco; `[⇆]` move foco entre corpos |

## 6. Relação com contratos

- `contrato_console.md`: autoridade do comportamento normativo completo do console.
- `contrato_barra_de_menus.md`: chips `[✥]`, `[␣]`, `[#]`, `[⏎]` são declarados pela barra.

## 7. Relação com ADRs

- ADR-0005: escopo de `[✥]` restrito a console.
- ADR-0006: renomeação `dado` para `console`.
- ADR-0026, ADR-0027, ADR-0028: dados externos e modos de apresentação do console.

## 8. Aliases ou termos descontinuados relacionados

- `dado` → termo descontinuado substituído por `console` (ADR-0006). Ver módulo `90`.

## 9. Conteúdo que não pertence a este módulo

- `grupo` como nó estrutural de composição do corpo → módulo `40`.
- Regras comportamentais completas de navegação → `contrato_console.md`.
- Apresentações multinível e modos verboso/não verboso → módulo `44`.
- Carregamento e associação de conteúdo externo → módulo `43`.
- Dados externos e envelope declarativo → módulo `42`.
- Pendência `tx` (regras de ajuste quando texto não cabe) → classificada como pendência
  no relatório de aplicação (NOM-LEV-017); sem decisão vigente.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§4.0 (linhas 359-398), §4.1-4.4 (linhas 399-531)"
  intervalo_ou_bloco: "NOM-LEV-009, NOM-LEV-010"
origem_normativa: ADR-0005, ADR-0006
contratos_relacionados:
  - contrato_console.md
  - contrato_barra_de_menus.md
adrs_relacionadas:
  - ADR-0005
  - ADR-0006
  - ADR-0026
  - ADR-0027
  - ADR-0028
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS:
  - "Pendência tx: regras de ajuste do texto quando não cabe — classificada como PENDENCIA (NOM-LEV-017)"
  - "Relação [#] × [␣]: explicitamente adiada, não é pendência normativa atual"
```
