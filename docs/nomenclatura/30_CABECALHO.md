---
name: nomenclatura-cabecalho
description: Terminologia do cabeçalho — região fixa superior da tela, campos textuais, schema de apresentação e limites declarativos
metadata:
  type: nomenclatura
  scope: cabecalho
  fase_de_aplicacao: VIGENTE
---

# Cabeçalho

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
- cabeçalho como região;
- título e descrição;
- limites declarativos;
- campos do cabeçalho;
- schema de apresentação de `titulo` e `descricao`;
- relação do cabeçalho com a tela.

## 3. Termos proprietários

- `cabecalho` (como região)
- `titulo` (campo do cabeçalho)
- `descricao` (campo do cabeçalho)
- `max_caracteres`
- campos de schema de `titulo`: `posicao`, `recuo_lateral`, `capitalizacao`, `formato_na_borda`
- campos de schema de `descricao`: `max_caracteres`, `alinhamento`, `recuo`, `capitalizacao`
- `config/elementos/cabecalho.json` (como arquivo de parâmetros de apresentação)

## 4. Definições

### 4.1 Cabeçalho como região

O `cabecalho` é a região fixa superior de toda tela do sistema. Sempre existe;
nunca ausente, condicional ou opcional.

O `cabecalho` não é corpo, não é `dashboard`, não é `lancador` e não é
`barra_de_menus`. Não herda regras de layout de nenhuma dessas regiões.

### 4.2 Campos textuais

| Campo | Função | Restrição |
|---|---|---|
| `titulo` | Texto curto de identificação da tela | Sem limite de caracteres definido — o estilo de apresentação é configurável via `config/elementos/cabecalho.json` |
| `descricao` | Texto longo de contextualização | Máximo de 200 caracteres (`max_caracteres` em `config/elementos/cabecalho.json`) |

Os textos concretos de `titulo` e `descricao` pertencem à classe/tela, não
ao JSON de configuração global. A classe declara o conteúdo textual;
`config/elementos/cabecalho.json` guarda somente os parâmetros de apresentação.

### 4.3 Schema de apresentação — `titulo`

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `posicao` | `esquerda` \| `centro` \| `direita` | Posição horizontal do bloco do título na linha da borda superior |
| `recuo_lateral` | inteiro ≥ 0 | Distância em caracteres do canto esquerdo (`esquerda`) ou direito (`direita`). Ignorado quando `posicao = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` | Transformação aplicada ao texto do `titulo` antes da renderização |
| `formato_na_borda` | `com_espacos_laterais` | Estilo de integração do título à linha da borda superior |

### 4.4 Schema de apresentação — `descricao`

| Campo | Valores permitidos | Semântica |
|---|---|---|
| `max_caracteres` | inteiro > 0 | Número máximo de caracteres; texto que exceder é truncado antes da renderização |
| `alinhamento` | `esquerda` \| `centro` \| `direita` | Alinhamento horizontal do texto da descrição |
| `recuo` | inteiro ≥ 0 | Distância em caracteres da borda esquerda (`esquerda`) ou direita (`direita`). Ignorado quando `alinhamento = centro`. |
| `capitalizacao` | `maiusculas` \| `inicio_de_frase` | Transformação aplicada ao texto da `descricao` antes da renderização |

### 4.5 Parametrização — `config/elementos/cabecalho.json`

Os parâmetros de apresentação do `cabecalho` vivem em
`config/elementos/cabecalho.json`, não hardcoded. O arquivo guarda os valores
concretos de apresentação. O arquivo não contém textos concretos de telas
(valores de `titulo` e `descricao`) — esses pertencem a cada classe/tela.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `cabecalho` × corpo | Cabeçalho é região fixa superior; corpo é a região variável do meio — regidas por contratos diferentes |
| `titulo` e `descricao` (conteúdo) × parâmetros de apresentação | Conteúdo pertence à classe/tela; parâmetros de apresentação ficam em `config/elementos/cabecalho.json` |

## 6. Relação com contratos

- `contrato_cabecalho.md`: autoridade do comportamento normativo completo.
- `contrato_tela_json.md`: o schema completo da tela inclui o `cabecalho`.

## 7. Relação com ADRs

- ADR-0022: define que a tela inicial real inclui `cabecalho`.

## 8. Aliases ou termos descontinuados relacionados

`config/elementos/cabecalho.json` é listado como ativo transicional no
monólito (status transitório registrado no relatório histórico). Como caminho
de artefato, sua classificação final pertence ao módulo `02`.

## 9. Conteúdo que não pertence a este módulo

- Schema completo do `tela.json` → `contrato_tela_json.md`.
- Corpo, `barra_de_menus` → módulos `20`, `31`.
- Comportamento normativo completo de renderização do cabeçalho →
  `contrato_cabecalho.md`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§7 (linhas 826-892)"
  intervalo_ou_bloco: "NOM-LEV-013"
origem_normativa: ADR-0022
contratos_relacionados:
  - contrato_cabecalho.md
  - contrato_tela_json.md
adrs_relacionadas:
  - ADR-0022
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
