# Relatório histórico: nomenclatura monolítica

**Data de criação**: 2026-07-20
**Fase**: PRE_FACHADA (ADR-0029, FASE_1_MATERIALIZACAO_PRE_FACHADA)
**Finalidade**: Preservar o registro histórico de instâncias concretas, nomes e
caminhos que não são definições universais — extraídos do monólito durante a
materialização da estrutura modular.

---

## 1. Propósito deste documento

Este relatório é o destino de conteúdo do monólito (`docs/NOMENCLATURA.md`)
classificado como `CLASSIFICADO_COMO_HISTORICO` durante a migração da FASE_1.

Conteúdo histórico não é definição universal e não pertence a nenhum módulo
terminológico. Este documento o preserva com rastreabilidade de origem,
sem suprimir nem generalizar.

O monólito permanece intacto como fonte normativa vigente durante o estado
PRE_FACHADA. Este relatório é complementar, não substitutivo.

---

## 2. Inventário de conteúdo histórico

### 2.1 Instância de referência: tela raiz do Orquestrador

**Origem**: §9 do monólito (linhas 987-1045), NOM-LEV-015

A tela raiz do Orquestrador é a instância concreta de `dashboard` mais
documentada no monólito. Seus valores não são definições universais.

**Marcadores da instância de referência**:

| Símbolo | Rótulo | Status no monólito |
|---|---|---|
| `!` | Retido | Ativo |
| `@` | Incompleto | Ativo |
| `?` | Ausência | Ativo |
| `*` | Revisão | Ativo |
| `&` | Dissonância | Ativo |
| `%` | Indevido | Ativo |
| `~` | Atualização | Ativo |
| `^` | Mesclado | Ativo |

**Campos de resumo da instância de referência** (8 campos):
Adicionados, Fichados, Consolidados, Qualificados, Orfão, Missing,
Secundários, Descartados.

> Estes campos são da instância raiz conhecida. Não definem a classe universal
> de `dashboard`.

---

### 2.2 Histórico de substituição terminológica: `menu` → `lancador`

**Origem**: §13 do monólito (linhas 1146-1215), NOM-LEV-020, DOC-0008, DOC-0009

| Item | Termo anterior | Termo atual | Data da substituição |
|---|---|---|---|
| Nome do tipo de elemento do corpo | `menu` | `lancador` | 2026-07-06 |

A decisão foi registrada em DOC-0008 e DOC-0009. O §13 do monólito documenta
a motivação da substituição e o rastreamento de consumidores afetados.

O tipo canônico `lancador` está definido no módulo `33`.
A substituição está registrada no módulo `90` (aliases e descontinuados).

---

### 2.3 Histórico de substituição terminológica: `Info` e `dado`

**Origem**: ADR-0006; §4 (console) e §9 (dashboard) do monólito

| Termo anterior | Termo atual | Módulo canônico | Decisão |
|---|---|---|---|
| `Info` | `dashboard` | `34` | ADR-0006 |
| `dado` (container navegável) | `console` | `32` | ADR-0006 |

---

### 2.4 Histórico de caminhos de configuração

**Origem**: ADR-0021; §2 do monólito (artefatos)

| Caminho histórico | Caminho canônico atual | Módulo canônico |
|---|---|---|
| `config/lancador.json` | `config/elementos/lancador.json` | `33` |
| `config/cabecalho.json` | `config/elementos/cabecalho.json` | `30` |

A migração de caminhos foi formalizada pela ADR-0021. O caminho histórico não
é mais o caminho normativo.

---

### 2.5 Pendências e itens classificados como `NAO_CONFIRMADO` no monólito

**Origem**: §11 do monólito (linhas 1074-1130), §4 (linhas 359-398), §9

Estes itens existem no monólito mas não têm decisão vigente confirmada.
Foram preservados como pendências, sem migração para os módulos terminológicos.

#### NOM-LEV-017 — Bloco geral de pendências em aberto (§11, linhas 1074-1101)

O bloco NOM-LEV-017 é o inventário geral de pendências em aberto do monólito.
Inclui todos os seguintes itens sem decisão vigente:

| Item pendente | Descrição |
|---|---|
| Pendência `tx` | Regras de ajuste do texto quando não cabe na coluna do console |
| `popup_execucao` | Janela temporária de saída de execução — sem definição aprovada |
| Alinhamento horizontal do `dashboard` | Falta decidir se acompanha o `lancador` (bloco à esquerda com sobra à direita) ou mantém centralização |
| Segunda pauta de estilos de exibição | Decisão deferida |
| Campos de navegação do lançador | Pendência de definição |
| Reorganização corpo × dashboard | Pendência de definição |

O alinhamento horizontal do dashboard é um item contido neste bloco geral.
Não é um bloco NOM-LEV separado.

#### NOM-LEV-018 — Levantamento Codex de legado (§11, linhas 1103-1130)

O bloco NOM-LEV-018 registra o levantamento histórico do Codex sobre o sistema
legado. Conteúdo de origem histórica, sem decisão normativa vigente:

| Item | Descrição |
|---|---|
| `teste_classe_c.py` | Arquivo do sistema legado localizado pelo Codex |
| `teste_combo.py` | Arquivo do sistema legado localizado pelo Codex |
| Relação `[#]` × `[␣]` | Explicitamente adiada; identificada no levantamento histórico |
| Wrap e outros legados | Demais referências históricas do levantamento |

#### NOM-LEV-019 — Lista parcial de ADRs aceitas (§12, linhas 1132-1142)

O bloco NOM-LEV-019 é o registro histórico da lista parcial de ADRs aceitas
que existia no monólito (seção 12), listando ADR-0001 a ADR-0004. Lista
histórica e parcial. A autoridade atual sobre a lista e estado de todas as
ADRs é `docs/adr/INDICE_ADR.md`.

**NOM-LEV-019 não representa alinhamento do dashboard nem pendência de interface.**

Estes itens **não foram transferidos para os módulos** por ausência de
confirmação normativa. O módulo proprietário deve aguardar decisão para receber
o conteúdo.

---

### 2.6 Status transitório de artefatos JSON (NOM-LEV-005)

**Origem**: §0 do monólito (linhas 89-105)

```yaml
bloco: NOM-LEV-005
secao_monolito: "§0, linhas 89-105"
conteudo: status_transitorio_de_artefatos_JSON
tratamento: ESTADO_TRANSITORIO_HISTORICO
modulo_proprietario: NAO_APLICAVEL
definicao_terminologica_ativa: false
```

A tabela de status dos artefatos JSON (linhas 89-101 do monólito) registrava
os estados transitórios de migração de arquivos como `layout_dado.json`,
`layout_menu.json` e `lancador.json`. Esses estados refletiam um momento de
transição, não uma terminologia vigente.

Este conteúdo é classificado como `ESTADO_TRANSITORIO_HISTORICO`. Não pertence
a nenhum módulo terminológico ativo. O módulo `02` registra que estados
transitórios de migração não são termos ativos e remete ao relatório histórico.

---

### 2.7 Decisões deferidas do §17 do monólito

**Origem**: §17 do monólito (linhas 1535-1615)

O §17 registra itens fora do escopo da ADR-0026 que foram explicitamente
deferidos para futura decisão:
- Distribuição multinível recursiva.
- Herança de campos entre níveis.
- Cascata de configuração de apresentação.
- Paginação do conjunto multinível.
- Migração automática de dados entre níveis.

Estes itens não têm ADR vigente e não foram migrados para nenhum módulo.

---

### 2.8 Divergência terminológica ativa: `modo normal` × `modo não verboso`

**Origem**: §19 do monólito (linhas 1721-1856), ADR-0028

A ADR-0028 registra a política de modo mas não reconcilia a divergência entre
`modo normal` (uso alternativo em documentos históricos) e `modo não verboso`
(uso predominante).

Ambos os termos são ativos e coexistem. A reconciliação está deferida para
nova ADR. Ver módulo `44` e módulo `90`.

---

## 3. Rastreabilidade

| Conteúdo histórico | Seção do monólito | NOM-LEV | Módulo de destino (se houver) |
|---|---|---|---|
| Marcadores e campos da tela raiz | §9 (987-1045) | NOM-LEV-015 | `34` (tipo universal); instância aqui |
| Histórico `menu` → `lancador` | §13 (1146-1215) | NOM-LEV-020 | `33` (tipo canônico), `90` (alias) |
| Histórico `Info` → `dashboard` | ADR-0006 | — | `34` (tipo canônico), `90` (alias) |
| Histórico `dado` → `console` | ADR-0006 | — | `32` (tipo canônico), `90` (alias) |
| Caminhos históricos de config | ADR-0021, §0 (linhas 57-87) | NOM-LEV-004 | `02` (artefatos), `90` |
| Pendência `tx` | §4, §11 | NOM-LEV-017 | Aguarda decisão |
| `popup_execucao` | §11 (1074-1101) | NOM-LEV-017 | Aguarda decisão; sem definição aprovada |
| Alinhamento horizontal do `dashboard` | §9, §11 (1074-1101) | NOM-LEV-017 | Aguarda decisão; contido no bloco geral NOM-LEV-017 |
| Levantamento Codex legado (`teste_classe_c.py`, `teste_combo.py`) | §11 (1103-1130) | NOM-LEV-018 | Histórico; sem módulo de destino |
| Relação `[#]` × `[␣]` | §11 (1103-1130) | NOM-LEV-018 | Histórico; explicitamente adiada |
| Lista parcial de ADRs (ADR-0001 a ADR-0004) | §12 (1132-1142) | NOM-LEV-019 | Histórica; autoridade atual: `docs/adr/INDICE_ADR.md` |
| Status transitório de artefatos JSON | §0 (89-105) | NOM-LEV-005 | ESTADO_TRANSITORIO_HISTORICO; sem módulo ativo |
| Decisões deferidas §17 | §17 (1535-1615) | — | Aguarda ADR |
| Divergência `modo normal` × `não verboso` | §19 (1721-1856) | NOM-LEV-028 | `44`, `90` |

---

## 4. Instruções para manutenção

- Este relatório é imutável quanto ao passado registrado. Novos itens históricos
  podem ser acrescentados em seções futuras.
- Quando uma pendência receber decisão, mover o conteúdo para o módulo
  proprietário e anotar neste documento com a referência à decisão.
- Quando a divergência terminológica `modo normal` × `modo não verboso` for
  resolvida por nova ADR, atualizar as seções 2.8 e 3 com referência à ADR.
- Não remover seções históricas — apenas marcar como `[RESOLVIDO: ADR-XXXX]`
  ao lado do item.
