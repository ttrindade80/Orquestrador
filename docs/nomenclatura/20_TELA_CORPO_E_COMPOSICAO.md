---
name: nomenclatura-tela-corpo-composicao
description: Terminologia de tela e regiões, elementos funcionais do corpo, composição genérica, arranjo, cardinalidade e relação conceitual com tiling
metadata:
  type: nomenclatura
  scope: tela_corpo_composicao
  fase_de_aplicacao: VIGENTE
---

# Tela, corpo e composição

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário de:
- tela e suas regiões (conceito genérico);
- cabeçalho e corpo como regiões;
- elemento funcional (definição de tipo);
- container estrutural (definição de tipo);
- filhos diretos;
- composição genérica;
- arranjo vertical e horizontal (conceito no container);
- cardinalidade;
- relação conceitual com tiling;
- composição hierárquica do corpo como árvore.

**Fronteiras obrigatórias**:
- `barra_de_menus` como região específica, instância e instância declarada:
  proprietário exclusivo é o módulo `31_BARRA_DE_MENUS_E_CHIPS.md`. Este
  módulo apenas cita `barra_de_menus` como região concreta da tela.
- `grupo` como nó estrutural, profundidade, distribuição de grupo:
  proprietário exclusivo é o módulo `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md`.
  Este módulo apenas cita `grupo` como espécie de container estrutural.

Não redefinir distribuição entre filhos, que pertence ao módulo `40`.

## 3. Termos proprietários

- tela
- cabeçalho (como região)
- corpo (como região)
- tipos de elemento do corpo: `console`, `lancador`, `dashboard` (identificação dos tipos)
- elemento funcional (classificação)
- container estrutural (classificação)
- filhos diretos
- `corpo.arranjo`
- arranjo vertical / horizontal (no contexto do container)
- cardinalidade (1 corpo / múltiplos corpos)
- composição declarativa
- `tela.json` (como declaração configurável — referência)
- espaço contíguo entre filhos
- tela de processamento como composição (ADR-0007)
- `ocupacao_vertical_terminal` (referenciado — definido no módulo `21`)
- `posicao_dashboard` (descontinuado — referenciado no módulo `90`)

Termos referenciados (não proprietários deste módulo):
- `barra_de_menus` — citada como região concreta da tela; proprietário: módulo `31`
- `grupo` — citado como espécie de container estrutural; proprietário: módulo `40`

## 4. Definições

### 4.1 Regiões da tela

Toda tela do sistema tem exatamente três regiões:

1. **Cabeçalho**: título + descrição. Proprietário terminológico: módulo `30`.
2. **Corpo**: estrutura variável — pode ter mais de um objeto, em arranjo
   vertical ou horizontal. Proprietário terminológico: este módulo.
3. **`barra_de_menus`**: região fixa inferior com chips de ação. Proprietário
   terminológico: módulo `31`.

### 4.2 Tipos de elemento do corpo

A taxonomia é fechada (ADR-0010, ADR-0007):

| Tipo | Natureza | Módulo proprietário |
|---|---|---|
| `console` | Container interativo e navegável genérico | módulo `32` |
| `lancador` | Elemento de navegação para outras telas | módulo `33` |
| `dashboard` | Saída passiva formatada | módulo `34` |
| `grupo` | Container estrutural (não elemento funcional) | módulo `40` |

Elementos funcionais: `console`, `lancador` e `dashboard`.
Container estrutural: `grupo`.

### 4.3 Composição declarativa do corpo

A composição do corpo é declarada pela classe de tela, nunca decidida pelo
renderer ou pela `barra_de_menus`.

| Eixo | Valores |
|---|---|
| Tipo de conteúdo | `console`, `lancador` |
| Tipo de exibição | `normal` (lista simples) / `verboso` (detalhes) — aplica-se apenas a `console` |
| Dashboard | presente / ausente |
| Quantidade de corpos | 1 corpo / múltiplos corpos |
| Arranjo de múltiplos corpos (opcional) | `vertical` / `horizontal` (ADR-0011) |
| Paginação | com / sem |
| Colunas ajustável (tipo `console`) | com / sem |
| `filtro_de_grupo` | `com` / `sem` |
| `formacao_de_selecao` | `com` / `sem` |
| Espaçamento interno | linha em branco entre borda e conteúdo |
| Organização horizontal | regra mínima por tipo de conteúdo |

### 4.4 Arranjo de múltiplos corpos

Quando a classe fixa o arranjo (`vertical` / `horizontal`), a preferência
global (`tiling`) é ignorada para aquela tela. Se a classe não fixar arranjo,
usa-se o campo `tiling` do estilo como default.

**Arranjo horizontal**: o espaço horizontal é particionado de forma contígua
entre os filhos diretos do container — sem vão externo entre eles (ADR-0015).
A área de um filho termina imediatamente onde a do próximo começa.

### 4.5 Tela de processamento como composição (ADR-0007)

Tela de processamento não é tipo de corpo. A taxonomia fechada do corpo
permanece `console`, `lancador`, `dashboard`. Uma tela de processamento é
descrita como composição de tipos existentes.

### 4.6 Composição hierárquica do corpo (ADR-0015)

O corpo é modelado como árvore, não lista plana de elementos.

| Conceito | Definição |
|---|---|
| Corpo como árvore de composição | O corpo é modelado como árvore, não lista plana |
| `arranjo` pertence ao container | Cada container (`corpo` ou `grupo`) declara o `arranjo` dos seus filhos diretos |
| `distribuicao` pertence ao container | `distribuicao` é atributo do container, não do filho |
| Filhos diretos | Somente filhos imediatos contam na distribuição; netos não entram |
| Espaço contíguo | A área de um filho termina imediatamente onde a do próximo começa |

A especificação normativa completa está em ADR-0015 e em
`contrato_composicao_corpo.md`.

### 4.7 `tela.json` como declaração configurável

`tela.json` é o nome canônico da declaração configurável de uma tela. Não
é código executável. Não guarda estado de runtime. Proprietário terminológico
do schema completo: `contrato_tela_json.md` e módulo `02`.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `corpo.arranjo = "vertical"` × `ocupacao_vertical_terminal` | Arranjo: composição dos elementos do corpo; ocupação vertical: preenchimento da altura da janela (ADR-0013) — definido no módulo `21` |
| `corpo.arranjo` × `tiling` | `corpo.arranjo` é arranjo fixado pela classe de tela; `tiling` é preferência global quando a classe não fixa |
| `corpo.arranjo` × `corpo.distribuicao` | Arranjo: ordem/composição dos filhos; distribuição: repartição proporcional da área — definida no módulo `40` |
| elemento funcional × container estrutural | Elementos funcionais produzem saída visual (`console`, `dashboard`, `lancador`); containers estruturais organizam outros nós (`grupo`) |
| `posicao_dashboard` × estrutura declarativa do `corpo` | `posicao_dashboard` está descontinuado como eixo separado (ADR-0010); posição do `dashboard` é controlada pela estrutura declarativa geral do `corpo` |

## 6. Relação com contratos

- `contrato_composicao_corpo.md`: autoridade do comportamento normativo completo.
- `contrato_tela_json.md`: schema completo do `tela.json`.

## 7. Relação com ADRs

- ADR-0007: tela de processamento como composição de tipos existentes.
- ADR-0010: composição hierárquica; `dashboard` como elemento funcional.
- ADR-0011: terminologia `vertical`/`horizontal` para arranjo.
- ADR-0013: distinção `corpo.arranjo` × `ocupacao_vertical_terminal`.
- ADR-0015: composição hierárquica e distribuição de área.
- ADR-0019: profundidade contada por grupos; multiplicidade estrutural.
- ADR-0024: proibição de espaço externo vazio.

## 8. Aliases ou termos descontinuados relacionados

- `sobreposto` → alias transitório de `vertical` → módulo `90`.
- `lado_a_lado` → alias transitório de `horizontal` → módulo `90`.
- `posicao_dashboard` → campo descontinuado como eixo independente (ADR-0010) → módulo `90`.

## 9. Conteúdo que não pertence a este módulo

- Distribuição entre filhos → módulo `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md`.
- Definição aprofundada de `grupo` → módulo `40`.
- Grandezas de largura e altura, redimensionamento → módulo `21`.
- Cabeçalho (schema) → módulo `30`.
- `barra_de_menus` (schema) → módulo `31`.
- Comportamento completo de `console` → módulo `32` e `contrato_console.md`.
- Comportamento completo de `lancador` → módulo `33` e `contrato_lancador.md`.
- Comportamento completo de `dashboard` → módulo `34`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§2 (linhas 234-327), §3 (linhas 328-358), §10 (linhas 1049-1072), §14 (linhas 1216-1287)"
  intervalo_ou_bloco: "NOM-LEV-007, NOM-LEV-008, NOM-LEV-016, NOM-LEV-021"
origem_normativa: ADR-0007, ADR-0010, ADR-0011, ADR-0013, ADR-0015, ADR-0019
contratos_relacionados:
  - contrato_composicao_corpo.md
  - contrato_tela_json.md
adrs_relacionadas:
  - ADR-0007
  - ADR-0010
  - ADR-0011
  - ADR-0013
  - ADR-0015
  - ADR-0019
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
  - REFERENCIADO
partes_NAO_CONFIRMADAS: []
```
