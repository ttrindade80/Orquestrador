---
name: nomenclatura-aliases-e-termos-descontinuados
description: Registro de aliases ativos e termos descontinuados — correspondência com termos canônicos, justificativa e módulo proprietário
metadata:
  type: nomenclatura
  scope: aliases_termos_descontinuados
  fase_de_aplicacao: VIGENTE
---

# Aliases e termos descontinuados

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário do **registro** de:
- aliases ativos (sinônimos aceitos em uso contemporâneo);
- termos descontinuados (substituídos por decisão de ADR ou decisão documental);
- histórico de substituição terminológica com rastreabilidade.

Não é proprietário das definições dos termos canônicos — cada definição vive
no módulo proprietário do domínio. Este módulo apenas registra a correspondência.

## 3. Tabela de aliases e termos descontinuados

### 3.1 Termos descontinuados por ADR

| Termo descontinuado | Termo canônico | Módulo canônico | Decisão | Observações |
|---|---|---|---|---|
| `Info` | `dashboard` | `34` | ADR-0006 | Renomeação: `Info` → `dashboard` |
| `dado` (container navegável) | `console` | `32` | ADR-0006 | Renomeação: `dado` → `console` |
| `menu` (corpo) | `lancador` | `33` | decisão documental 2026-07-06 | Ver seção 3.3 |

### 3.2 Aliases ativos (sinônimos aceitos)

| Alias | Termo canônico | Módulo canônico | Decisão | Observações |
|---|---|---|---|---|
| `lado_a_lado` | `sobreposto` | `10` | Sem decisão formal registrada | Alias de estilo para tiling; substituição não formalizada como ADR |
| `sobreposto` | `lado_a_lado` | `10` | Idem | Ambos em uso; sem prioridade decidida |

> **Nota sobre `lado_a_lado` × `sobreposto`**: a relação entre esses dois termos
> de tiling não possui ADR ou decisão formal registrada. O §10 do monólito
> menciona ambos sem estabelecer hierarquia. Registrado como **alias com
> divergência não formalizada** até que uma ADR resolva.

### 3.3 Histórico de mudança: `menu` para `lancador`

A substituição de `menu` (corpo) por `lancador` foi decidida em 2026-07-06,
registrada nos documentos e no §13 do monólito (`docs/NOMENCLATURA.md`,
linhas 1146-1215), referenciando DOC-0008 e DOC-0009.

| Item | Antes | Depois |
|---|---|---|
| Nome do tipo de elemento | `menu` | `lancador` |
| Caminho de configuração | `config/lancador.json` (path inicial) | `config/elementos/lancador.json` (ADR-0021) |

O caminho `config/lancador.json` foi o caminho inicial histórico; a migração
para `config/elementos/lancador.json` foi formalizada pela ADR-0021.

### 3.4 Migração de caminhos de configuração (ADR-0021)

| Caminho histórico | Caminho canônico atual | Módulo canônico | Decisão |
|---|---|---|---|
| `config/lancador.json` | `config/elementos/lancador.json` | `33` | ADR-0021 |
| `config/cabecalho.json` | `config/elementos/cabecalho.json` | `30` | ADR-0021 |

## 4. Termos com divergência ativa (não descontinuados, não reconciliados)

| Termo A | Termo B | Módulo | Status |
|---|---|---|---|
| `modo normal` | `modo não verboso` | `44` | Dois termos coexistentes para o mesmo conceito; reconciliação deferida para nova ADR (ADR-0028 registra mas não resolve) |
| `sobreposto` | `lado_a_lado` | `10` | Alias com divergência não formalizada; ambos em uso ativo |

**Regra de leitura para divergências ativas**: não substituir um pelo outro até
que nova ADR decida. Ao documentar, usar o termo da fonte que está sendo lida.

## 4A. Termos concorrentes deferidos localizáveis

Estes termos aparecem em documentação de origem (ADR-0028 e fontes históricas)
mas **não são termos canônicos ativos confirmados** nem aliases aprovados.
Registram disputas terminológicas abertas com o schema vigente. Estão aqui
para garantir que sejam localizáveis, não para declarar prevalência.

| Termo concorrente | Correspondência no schema | Domínio | Módulo de referência | Estado |
|---|---|---|---|---|
| `folha` | `conteudo` | dados externos multinível | `42_DADOS_EXTERNOS_MULTINIVEL.md` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL |
| `campo` | `nome_valor` | dados externos multinível | `42_DADOS_EXTERNOS_MULTINIVEL.md` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL |
| `hierarquia_indentada` | `hierarquia` | apresentações multinível | `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | TERMO_CONCORRENTE_DEFERIDO_LOCALIZAVEL |

Estes termos não integram a contagem de termos ativos nem de aliases aprovados.
Integram a contagem separada de `termos_concorrentes_deferidos`. Nenhum campo
de schema deve ser renomeado com base neles. A reconciliação requer nova ADR.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| alias ativo × termo descontinuado | Alias ativo: sinônimo aceito contemporâneo; descontinuado: substituído por decisão, não deve ser usado em documentos novos |
| descontinuado × divergência ativa | Descontinuado: decisão tomada, termo antigo; divergência ativa: dois termos coexistentes sem decisão tomada |

## 6. Relação com contratos

Este módulo não possui relação direta com contratos. Os termos canônicos são
referenciados nos contratos; as substituições são documentadas aqui.

## 7. Relação com ADRs

- ADR-0006: renomeação `Info` → `dashboard`; `dado` → `console`.
- ADR-0021: migração de caminhos de configuração para `config/elementos/`.
- ADR-0028: modos do console — divergência `modo normal` × `modo não verboso` não resolvida.

## 8. Conteúdo que não pertence a este módulo

- Definições dos termos canônicos → módulos proprietários do domínio.
- Regras comportamentais → contratos.
- Histórico de instâncias concretas → `RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md`.

## 9. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§1 (aliases tiling), §8 (lançador), §13 (menu→lancador), §17-18 (modos do console)"
  intervalo_ou_bloco: "NOM-LEV-001 a NOM-LEV-028 (registros de aliases dispersos)"
origem_normativa: ADR-0006, ADR-0021, ADR-0028
contratos_relacionados: []
adrs_relacionadas:
  - ADR-0006
  - ADR-0021
  - ADR-0028
tratamento:
  - PRESERVADO
  - CLASSIFICADO_COMO_HISTORICO
partes_NAO_CONFIRMADAS:
  - "Relação lado_a_lado × sobreposto: alias com divergência não formalizada (sem ADR)"
```
