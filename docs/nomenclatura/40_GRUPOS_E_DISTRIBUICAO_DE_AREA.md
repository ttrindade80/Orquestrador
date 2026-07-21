---
name: nomenclatura-grupos-e-distribuicao-de-area
description: Terminologia de grupo como nó estrutural, profundidade, aninhamento, distribuição entre filhos, modos de distribuição, ausência de distribuição, ocupação integral, espaço externo, grupo livre e matriz de grupos
metadata:
  type: nomenclatura
  scope: grupos_distribuicao_area
  fase_de_aplicacao: VIGENTE
---

# Grupos e distribuição de área

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
- grupo como nó estrutural;
- profundidade e aninhamento;
- distribuição entre filhos diretos;
- modos de distribuição (`igual`, `percentual`, `fracao`, `restrito`, `dinamico`);
- ausência de distribuição (semântica);
- ocupação integral;
- espaço externo proibido;
- grupo livre;
- matriz de grupos;
- coordenada explícita de grupo.

Não redefinir composição geral do corpo, que pertence ao módulo `20`.

## 3. Termos proprietários

- `grupo` (como nó estrutural)
- profundidade hierárquica
- nível de grupo (1, 2, 3)
- nível de grupo 3 como máximo
- distribuição entre filhos diretos
- `corpo.distribuicao`
- modo `igual`
- modo `percentual`
- modo `fracao`
- ausência de distribuição (não equivale a `igual`)
- distribuição explícita
- cardinalidade unitária (DA-01)
- composição inválida (DA-02)
- grupo como container (DA-03)
- invariante impossível / rejeição (DA-04)
- espaço externo proibido
- espaço interno (permitido)
- elemento visual (como classificação)
- `estrutura: "livre"`
- `estrutura: "matriz"`
- `matriz de grupos`
- `linha da matriz`, `coluna da matriz`, `célula da matriz`
- coordenada explícita
- distribuição de linhas / distribuição de colunas (na matriz)
- grade comum
- cobertura completa

## 4. Definições

### 4.1 Grupo como nó estrutural (ADR-0015, ADR-0019)

`grupo` é nó estrutural de composição; não é tipo funcional. Não tem borda
própria, título visual, ação, item, origem de dados ou `tela_destino`.

Os elementos funcionais válidos são: `console`, `dashboard`, `lancador`. A lista
é fechada.

### 4.2 Profundidade (ADR-0019)

A profundidade hierárquica é contada exclusivamente pelo aninhamento de nós
estruturais `grupo`. O corpo raiz não conta como nível de grupo.

| Nível | Definição |
|---|---|
| Nível de grupo 1 | `grupo` filho direto de `corpo.elementos[]` |
| Nível de grupo 2 | `grupo` filho de um grupo do nível 1 |
| Nível de grupo 3 | Profundidade máxima; `grupo` filho de um grupo do nível 2 |

Estruturas com grupo no nível 4 ou superior são rejeitadas com erro estrutural
determinístico. Elementos funcionais dentro de um grupo do nível 3 não
constituem nível 4.

### 4.3 Distribuição entre filhos (ADR-0015, ADR-0018)

`distribuicao` é atributo do container, não do filho. Reparte área entre filhos
diretos apenas quando declarada.

**Modos previstos:**

| Modo | Semântica |
|---|---|
| `igual` | Divide a área igualmente entre filhos diretos |
| `percentual` | Soma diferente de 100 é erro de configuração |
| `fracao` | Pesos positivos; `[1,1,1]` = `1/3`, `1/3`, `1/3` |
| `restrito` | Previsto |
| `dinamico` | Previsto |

**Ausência de `corpo.distribuicao` ≠ modo `igual`** (ADR-0018): quando
`corpo.distribuicao` não é declarada, cada filho usa sua altura natural.
A ausência não é fallback do modo `igual`.

**Arredondamento**: usa maiores restos, de forma determinística. Soma final deve
ser exatamente igual à área disponível.

### 4.4 Espaço externo proibido e espaço interno (ADR-0024)

| Termo | Definição normativa |
|---|---|
| elemento visual | Nó de corpo do tipo `console`, `dashboard` ou `lancador` — taxonomia fechada |
| grupo | Nó estrutural de agrupamento; não é elemento visual; não pode justificar área vazia |
| espaço externo proibido | Linhas, colunas ou células fora das molduras dos elementos visuais, pertencentes apenas ao corpo ou container estrutural; proibido pelo renderer |
| espaço interno | Linhas em branco **dentro** da moldura de um elemento visual, resultado de distribuição explícita com cota maior que o conteúdo — permitido |
| cardinalidade unitária (DA-01) | Um único descendente visual ocupa integralmente toda a área disponível mesmo sem `distribuicao` declarada |
| composição inválida (DA-02) | Dois ou mais elementos disputam o mesmo eixo sem `distribuicao` declarada — rejeitada explicitamente |
| grupo não justifica área (DA-03) | Toda área atribuída a grupo deve ser repassada aos descendentes visuais |
| invariante impossível (DA-04) | Quando o invariante não pode ser satisfeito, a composição é rejeitada com erro identificável; sem fallback silencioso |

### 4.5 Comportamento `livre` e `matriz` do grupo (ADR-0020)

O campo `estrutura` é o seletor declarativo do comportamento de um nó `grupo`:

| Valor | Comportamento |
|---|---|
| `"livre"` | Comportamento hierárquico unidimensional — `arranjo` e `distribuicao` local por container |
| `"matriz"` | Comportamento bidimensional com grade comum, distribuições independentes por eixo e coordenadas explícitas de células |
| (ausente) | Equivale a `"livre"` — compatibilidade retroativa integral |

**`matriz de grupos`**: especialização do nó `grupo` que organiza os filhos
diretos em grade bidimensional com grade comum de coordenadas.

| Termo | Definição |
|---|---|
| `linha da matriz` | Faixa horizontal da grade |
| `coluna da matriz` | Faixa vertical da grade |
| `célula da matriz` | Interseção de linha e coluna; contém exatamente um filho direto |
| `coordenada explícita` | Par `(linha, coluna)` com índices iniciados em 1 |
| `distribuição de linhas` | Campo `matriz.linhas.distribuicao` — obrigatório em `estrutura: matriz` |
| `distribuição de colunas` | Campo `matriz.colunas.distribuicao` — obrigatório em `estrutura: matriz` |
| `grade comum` | Única grade de coordenadas compartilhada por todas as células |
| `cobertura completa` | Toda coordenada válida deve ser preenchida e todo filho direto deve estar associado exatamente uma vez |

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `grupo` (nó estrutural) × `grupo` (sentido do dado) | Nó estrutural de composição do corpo (este módulo) × origem/categoria do dado no console (módulo `32`) — requerem contexto |
| `corpo.distribuicao` × `corpo.arranjo` | Distribuição: repartição proporcional da área; arranjo: ordem/composição dos filhos |
| ausência de distribuição × modo `igual` | Ausência: cada filho usa altura natural (ADR-0018); `igual`: divisão proporcional explícita |
| `matriz de grupos` (ADR-0020) × `distribuição matricial` (ADR-0025) | Grupos: grade do nó estrutural; distribuição matricial: organização interna dos participantes de um elemento funcional (módulo `41`) |
| espaço externo proibido × espaço interno | Externo: fora das molduras dos elementos visuais (proibido); interno: dentro da moldura de elemento visual com distribuição (permitido) |

## 6. Relação com contratos

- `contrato_composicao_corpo.md`: autoridade do comportamento normativo completo.

## 7. Relação com ADRs

- ADR-0015: composição hierárquica; distribuição; arredondamento.
- ADR-0018: semântica da ausência de distribuição; ausência ≠ `igual`.
- ADR-0019: profundidade contada por grupos; multiplicidade estrutural.
- ADR-0020: comportamentos `livre` e `matriz`; coordenadas explícitas.
- ADR-0024: espaço externo proibido; DA-01 a DA-04.

## 8. Aliases ou termos descontinuados relacionados

Nenhum neste módulo.

## 9. Conteúdo que não pertence a este módulo

- Composição geral do corpo e regiões → módulo `20`.
- Distribuição matricial de nível único dos participantes de um elemento →
  módulo `41`.
- `grupo` como origem do dado no console → módulo `32`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§14.1-14.2 (linhas 1288-1370), §15 (linhas 1371-1447), §14 parcial (linhas 1216-1287)"
  intervalo_ou_bloco: "NOM-LEV-022, NOM-LEV-023, NOM-LEV-021 (parcial)"
origem_normativa: ADR-0015, ADR-0018, ADR-0019, ADR-0020, ADR-0024
contratos_relacionados:
  - contrato_composicao_corpo.md
adrs_relacionadas:
  - ADR-0015
  - ADR-0018
  - ADR-0019
  - ADR-0020
  - ADR-0024
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
