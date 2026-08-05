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
- `apresentacao` como bloco estrutural local do cabeçalho;
- `apresentacao.titulo` e `apresentacao.descricao` como subobjetos locais;
- limites declarativos;
- campos do cabeçalho;
- schema de apresentação de `titulo` e `descricao`;
- relação do cabeçalho com a tela.

## 3. Termos proprietários

- `cabecalho` (como região)
- `titulo` (campo do cabeçalho)
- `descricao` (campo do cabeçalho)
- `apresentacao` (bloco estrutural local do cabeçalho)
- `apresentacao.titulo`
- `apresentacao.descricao`
- `max_caracteres`
- campos de schema de `titulo`: `posicao`, `recuo_lateral`, `capitalizacao`, `formato_na_borda`
- campos de schema de `descricao`: `max_caracteres`, `alinhamento`, `recuo`, `capitalizacao`

## 4. Definições

### 4.1 Cabeçalho como região

O `cabecalho` é a região fixa superior de toda tela do sistema. Sempre existe;
nunca ausente, condicional ou opcional.

O `cabecalho` não é corpo, não é `dashboard`, não é `lancador` e não é
`barra_de_menus`. Não herda regras de layout de nenhuma dessas regiões.

### 4.2 Campos textuais

| Campo | Função | Restrição |
|---|---|---|
| `titulo` | Conteúdo textual curto de identificação da tela | Tipo, limites e semântica definidos em `contrato_cabecalho.md` |
| `descricao` | Conteúdo textual longo de contextualização | Tipo, limites e semântica definidos em `contrato_cabecalho.md` |

Os textos concretos de `titulo` e `descricao` pertencem à classe/tela, não
ao estilo global. A classe/tela declara o conteúdo textual e os parâmetros
locais de apresentação no objeto `cabecalho` de seu JSON estrutural.

### 4.3 Apresentação como bloco estrutural local

`apresentacao` é o bloco estrutural local obrigatório de `cabecalho`. Ele
contém somente parâmetros declarativos locais de apresentação; não contém
conteúdo textual, estado vivo, aparência global, aliases ou valores implícitos.

No JSON estrutural da tela, `cabecalho` contém exatamente os três campos
diretos obrigatórios `titulo`, `descricao` e `apresentacao`.

`apresentacao.titulo` e `apresentacao.descricao` são subobjetos obrigatórios.
`apresentacao.titulo` contém exatamente `posicao`, `recuo_lateral`,
`capitalizacao` e `formato_na_borda`. `apresentacao.descricao` contém
exatamente `max_caracteres`, `alinhamento`, `recuo` e `capitalizacao`.

Os tipos, enumerações, limites, semântica, validações e critérios de erro
desses campos pertencem exclusivamente a `docs/contratos/contrato_cabecalho.md`;
este módulo não os redefine.

Assim, `titulo` e `descricao` continuam sendo conteúdo textual, enquanto
`apresentacao` contém somente parâmetros declarativos locais.

### 4.4 Schema de apresentação — `titulo`

Os nomes dos campos de `apresentacao.titulo` são:

| Campo |
|---|
| `posicao` |
| `recuo_lateral` |
| `capitalizacao` |
| `formato_na_borda` |

`inicio_de_frase` é um valor de capitalização local do cabeçalho. Ele se
distingue de `maiusculas` porque transforma somente o primeiro caractere
alfabético, preservando o restante do texto. O critério de "caractere
alfabético" é `str.isalpha()` da linguagem Python, aplicado de forma
independente de locale e sem normalização Unicode prévia; a substituição usa
o resultado exato de `str.upper()` do Python sobre esse único caractere,
podendo produzir mais de um caractere Unicode. O algoritmo completo, a ordem
das etapas, os exemplos normativos — inclusive os casos de expansão da
conversão — e o tratamento dos casos-limite pertencem exclusivamente ao
contrato em `docs/contratos/contrato_cabecalho.md`, que permanece a
autoridade comportamental.

Os valores permitidos e a semântica desses campos são definidos no contrato
do cabeçalho.

### 4.5 Schema de apresentação — `descricao`

Os nomes dos campos de `apresentacao.descricao` são:

| Campo |
|---|
| `max_caracteres` |
| `alinhamento` |
| `recuo` |
| `capitalizacao` |

`apresentacao.descricao.max_caracteres` possui domínio de inteiro entre `1` e
`200`, inclusive, conforme o contrato do cabeçalho.

`apresentacao.descricao.capitalizacao` declara exatamente os valores
`maiusculas`, `inicio_de_frase` e `preservar`. `preservar` é a operação
identidade sobre o texto da descrição depois do corte por `max_caracteres`: a
etapa de capitalização mantém o texto exatamente como se encontra. A escolha
concreta pertence à tela. O algoritmo completo, a ordem, os exemplos
normativos e os casos-limite pertencem exclusivamente ao contrato em
`docs/contratos/contrato_cabecalho.md`, que é a autoridade comportamental; esta
nomenclatura não cria definição concorrente.

`preservar` representa apresentação local sem transformação de caixa. Uma
migração que pretende conservar literalmente a descrição anteriormente
renderizada deve declarar `preservar`. `inicio_de_frase` permanece disponível
como escolha explícita para telas que desejem essa transformação. A ausência
de `apresentacao.descricao.capitalizacao` é inválida.

### 4.6 Parametrização local no JSON estrutural da tela

Os parâmetros locais de apresentação do `cabecalho` vivem no objeto
`cabecalho` do JSON estrutural de cada tela, não hardcoded e não em
`config/estilo.json`. O objeto guarda os valores concretos de apresentação
junto aos textos concretos de `titulo` e `descricao` da tela.

### 4.7 Estado vivo de runtime e fronteiras declarativas

O estado vivo do `cabecalho` pertence à execução. Valores produzidos ou
mantidos durante a execução não são armazenados como estado vivo no JSON
estrutural da tela nem em `config/estilo.json`.

```yaml
json_estrutural_da_tela:
  responsabilidade:
    - textos concretos de titulo e descricao
    - parametros locais declarativos de apresentacao do cabecalho

config_estilo_json:
  responsabilidade:
    - aparencia global compartilhada aplicavel ao cabecalho e demais elementos

estado_vivo_de_runtime:
  responsabilidade:
    - valores produzidos ou mantidos durante a execucao
  pertence_ao_json_da_tela: false
  pertence_ao_config_estilo_json: false
```

A definição geral de `estado de runtime` deve ser consultada em
`docs/nomenclatura/01_NUCLEO_COMUM.md` e
`docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`. O
`docs/contratos/contrato_cabecalho.md` permanece a autoridade do comportamento
normativo completo do cabeçalho.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `cabecalho` × corpo | Cabeçalho é região fixa superior; corpo é a região variável do meio — regidas por contratos diferentes |
| `titulo` e `descricao` (conteúdo) × parâmetros locais de apresentação | Conteúdo e parâmetros locais pertencem ao JSON estrutural de cada tela; aparência global compartilhada pertence a `config/estilo.json` |

## 6. Relação com contratos

- `contrato_cabecalho.md`: autoridade completa do schema e do comportamento
  normativo do cabeçalho.
- `contrato_tela_json.md`: o schema completo da tela inclui o `cabecalho`.

## 7. Relação com ADRs

- ADR-0008: define o JSON por tela como fonte dos textos concretos e dos parâmetros locais de apresentação do cabeçalho, preservando `config/estilo.json` como biblioteca global de aparência.
- ADR-0022: define que a tela inicial real inclui `cabecalho`.

## 8. Aliases ou termos descontinuados relacionados

O caminho anteriormente associado a parâmetros globais do cabeçalho não é
termo proprietário nem fonte vigente. A classificação de artefatos e caminhos
pertence ao módulo `02`.

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
origem_normativa: ADR-0008, ADR-0022
contratos_relacionados:
  - contrato_cabecalho.md
  - contrato_tela_json.md
adrs_relacionadas:
  - ADR-0008
  - ADR-0022
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
