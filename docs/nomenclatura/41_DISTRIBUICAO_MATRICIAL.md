---
name: nomenclatura-distribuicao-matricial
description: Terminologia da distribuição matricial de elemento funcional — formação, margem, vão, nível único, formação responsiva e fixa, participantes imediatos, fallback matricial
metadata:
  type: nomenclatura
  scope: distribuicao_matricial
  fase_de_aplicacao: VIGENTE
---

# Distribuição matricial

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
- distribuição matricial de elemento funcional;
- formação (`preferencia_linhas`, `preferencia_colunas`, `matriz_fixa`);
- margem (no contexto da distribuição matricial);
- vão (no contexto da distribuição matricial);
- nível único;
- formação responsiva;
- formação fixa;
- participantes imediatos;
- fallback matricial.

Não confundir com `matriz de grupos` (ADR-0020, nó estrutural `grupo`) nem
com matriz interna do lançador (ADR-0001).

## 3. Termos proprietários

- `distribuicao_matricial` (campo declarativo do elemento)
- `distribuição matricial de nível único`
- elemento organizador
- participante imediato
- formação
- `preferência por linhas` (`preferencia_linhas`)
- `preferência por colunas` (`preferencia_colunas`)
- `matriz fixa` (`matriz_fixa`)
- célula (contexto ADR-0025)
- margem (contexto ADR-0025)
- vão (contexto ADR-0025)
- espaço excedente
- distribuição uniforme
- alinhamento interno
- formação válida
- impossibilidade geométrica
- recuperação determinística

## 4. Definições

### 4.1 Distribuição matricial de nível único (ADR-0025)

Capacidade genérica de organizar os participantes imediatos de um elemento
funcional em uma grade configurável, dentro da área útil daquele elemento.

| Termo | Definição normativa |
|---|---|
| `distribuição matricial de nível único` | Capacidade de organizar os participantes imediatos de um elemento em grade configurável, dentro da área útil daquele elemento |
| `elemento organizador` | Elemento funcional (`dashboard`, `console` ou `lancador`) que organiza diretamente o conjunto de participantes e declara `distribuicao_matricial` em seu JSON |
| `participante imediato` | Cada unidade do conjunto ordenado organizado pelo elemento no nível atual; perante o nível externo é tratado como unidade única |

### 4.2 Formação

Decisão de como os participantes são distribuídos em linhas e colunas:

| Formação | Comportamento |
|---|---|
| `preferencia_linhas` | Política de formação que prioriza preenchimento ao longo das linhas, respeitando limites declarados e a área disponível |
| `preferencia_colunas` | Política de formação que prioriza preenchimento ao longo das colunas |
| `matriz_fixa` | Exige a quantidade declarada de linhas e colunas; sem redução ou reorganização silenciosa — se não couber, aciona o estado canônico |

### 4.3 Espaçamento

| Termo | Definição |
|---|---|
| `margem` (ADR-0025) | Distância entre a borda da área útil do elemento e o início da grade matricial; medida interna ao elemento |
| `vão` (ADR-0025) | Distância entre colunas da grade (horizontal) ou entre linhas da grade (vertical) |
| `espaço excedente` | Diferença entre a área útil e a área mínima necessária para a formação válida |
| `distribuição uniforme` | Política que reparte o espaço excedente igualmente entre margens e vãos de um eixo |

### 4.4 Alinhamento e posicionamento

| Termo | Definição |
|---|---|
| `alinhamento interno` | Posição do participante dentro da célula que lhe foi alocada — horizontal (`inicio`, `centro`, `fim`) e vertical (`topo`, `centro`, `base`) |
| `formação válida` | Formação capaz de acomodar todos os participantes e todos os mínimos declarados dentro da área útil disponível |
| `impossibilidade geométrica` | Condição em que nenhuma formação válida consegue acomodar todos os participantes e todos os mínimos; aciona o estado canônico |
| `recuperação determinística` | Processo de reconstrução da distribuição válida quando a área volta a ser suficiente |

### 4.5 Fallback (impossibilidade geométrica)

O estado exibido quando ocorre impossibilidade geométrica é o `quadro mínimo de
terminal pequeno` já estabelecido pela ADR-0017 e ADR-0023 (definição no módulo `21`).

Nenhuma variante concorrente de quadro mínimo é criada para impossibilidade
geométrica por distribuição matricial.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `distribuicao_matricial` × `distribuicao` (área) | `distribuicao_matricial` organiza participantes dentro da área útil de um elemento; `distribuicao` (ADR-0015, ADR-0018) aloca área entre filhos diretos de um container estrutural |
| `participante imediato` × filho de `grupo` | Participante imediato: unidade perante o elemento organizador funcional; filho de `grupo`: filho de nó estrutural |
| `matriz de grupos` (ADR-0020) × `distribuição matricial` (ADR-0025) | ADR-0020: grade do nó estrutural `grupo`; ADR-0025: organização interna dos participantes de um elemento funcional |
| `nível único` × multinível | Nível único: apenas participantes imediatos; multinível: composição recursiva entre níveis — fora do escopo |
| `margem interna` × `espaço externo proibido` | Margem interna: distância configurável dentro da área útil do elemento; espaço externo proibido: linha ou coluna fora das molduras dos elementos visuais (ADR-0024) |
| `formação` × `ordem` | Formação: como os participantes são distribuídos em linhas e colunas; ordem: sequência em que posições são mapeadas para células |
| `alinhamento interno` × `distribuição horizontal/vertical` | Alinhamento: posição dentro da célula; distribuição horizontal/vertical: posição da grade inteira na área útil |

## 6. Relação com contratos

O vocabulário de campos de `distribuicao_matricial` está definido nos contratos
JSON de cada elemento:
- `contrato_json_console.md`
- `contrato_tela_json.md` (seção 30)

## 7. Relação com ADRs

- ADR-0025: capacidade genérica de distribuição matricial configurável de nível único.

## 8. Aliases ou termos descontinuados relacionados

Nenhum neste módulo.

## 9. Conteúdo que não pertence a este módulo

- `matriz de grupos` (nó estrutural `grupo`) → módulo `40`.
- Matriz interna do lançador (cálculo automático de colunas) → módulo `33`.
- Distribuição de área entre filhos de container → módulo `40`.
- Itens fora do escopo da ADR-0025 (distribuição multinível, recursão, herança,
  cascata, paginação do conjunto, migração automática) → relatório histórico.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§16 (linhas 1448-1534)"
  intervalo_ou_bloco: "NOM-LEV-024"
origem_normativa: ADR-0025
contratos_relacionados:
  - contrato_json_console.md
  - contrato_tela_json.md
adrs_relacionadas:
  - ADR-0025
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
