---
name: relatorio-aplicacao-adr-0025
description: Relatório de aplicação da ADR-0025 — distribuição matricial configurável de nível único do conteúdo dos elementos
metadata:
  type: relatorio
  categoria: APLICAR_ADR
  adr: ADR-0025
  data: "2026-07-16"
  status: concluida
---

# Relatório de Aplicação — ADR-0025

**ADR:** ADR-0025 — Distribuição matricial configurável de nível único do conteúdo dos elementos
**Data:** 2026-07-16
**Executado por:** Assistente (Claude Sonnet 4.6)
**Categoria:** APLICAR_ADR

---

## 1. Entrada

**QA de entrada:** `RELATORIO_QA_POS_PATCH_ADR-0025.md`
**Resultado:** `ADR_APPROVED_WITH_NOTES`
**Achados bloqueantes:** 0
**Achados altos:** 0
**Achados médios:** 0
**Achados baixos:** 0
**Observações mantidas:** 3

| ID | Descrição |
|---|---|
| OBS-ADR0025-001 | Reconciliação com políticas específicas de `lancador`/`console`/`dashboard` |
| OBS-ADR0025-002 | "terminal muito pequeno" vs. `quadro mínimo de terminal pequeno` |
| OBS-ADR0025-POS-001 | "ponto de entrada real" em seção 38 é genérico, não vinculante |

---

## 2. Escopo autorizado

Arquivos permitidos para modificação:

- `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md` (este arquivo — criado)

---

## 3. Ações realizadas

### 3.1 ADR-0025 — Atualização de status

**Arquivo:** `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md`

- Frontmatter `status`: `aceita` → `aceita e aplicada`
- Tabela de identificação (seção 1): `| Status | aceita |` → `| Status | aceita e aplicada |`
- Seção 2: `` `aceita` `` → `` `aceita e aplicada` ``

Decisões do ADR não foram alteradas.

### 3.2 INDICE_ADR.md — Entrada ADR-0025

**Arquivo:** `docs/adr/INDICE_ADR.md`

Adicionada linha após ADR-0024:

```
| ADR-0025 | Distribuição matricial configurável de nível único do conteúdo dos
elementos — capacidade genérica adotável explicitamente por dashboard, console
e lancador; campo distribuicao_matricial no JSON do elemento organizador;
formação responsiva e fixa; ordem, dimensionamento, espaçamento, distribuição,
alinhamento e fallback independentes; nível único; paginação e multinível fora
do escopo; JSONs existentes não mudam silenciosamente; políticas específicas de
lancador (ADR-0001, ADR-0002, ADR-0003) preservadas | aceita e aplicada | 2026-07-16 |
```

### 3.3 NOMENCLATURA.md — Seção 16

**Arquivo:** `docs/NOMENCLATURA.md`

Adicionada seção 16 com subseções 16.1 a 16.5:

- **16.1 Termos fundamentais** — tabela de 15 termos canônicos com definições
  e distinções obrigatórias
- **16.2 Termos canonizados para o fallback** — reconcilia "terminal muito
  pequeno" (condição geométrica) com `quadro mínimo de terminal pequeno`
  (estado canônico exibido); resolve OBS-ADR0025-002
- **16.3 Distinções obrigatórias** — 7 pares de termos com distinção normativa
- **16.4 Vocabulário normativo dos campos** — remissão aos contratos JSON e
  exigência de atualização normativa antes de uso
- **16.5 Itens fora do escopo da ADR-0025** — 9 itens explicitamente fora de
  escopo ou proibidos

### 3.4 contrato_tela_json.md — Seção 30

**Arquivo:** `docs/contratos/contrato_tela_json.md`

- Frontmatter `adrs_aplicadas`: adicionada ADR-0025
- Adicionada seção 30 com subseções 30.1 a 30.9:
  - **30.1** Capacidade declarativa genérica — optional, adoção explícita
  - **30.2** Local declarativo — `corpo.elementos[] > elemento > distribuicao_matricial`
  - **30.3** Escopo de nível único — proibições explícitas (recursão, herança,
    cascata, multinível)
  - **30.4** Área útil — margens internas vs. preenchimento externo proibido (ADR-0024)
  - **30.5** Compatibilidade — sem migração automática, sem default estrutural
  - **30.6** Paginação fora do escopo — 6 itens explicitamente excluídos
  - **30.7** Fallback — `quadro mínimo de terminal pequeno`; 9 proibições no estado de fallback
  - **30.8** Elementos autorizados — `dashboard`, `console`, `lancador`
  - **30.9** Remissões — contratos específicos e NOMENCLATURA.md seção 16

### 3.5 contrato_composicao_corpo.md — Seção 11

**Arquivo:** `docs/contratos/contrato_composicao_corpo.md`

- Frontmatter `adrs_aplicadas`: adicionada ADR-0025
- Adicionada seção 11 com subseções 11.1 a 11.4:
  - **11.1** Separação de responsabilidades — tabela de três capacidades distintas
  - **11.2** O que a ADR-0025 não altera — 8 itens que permanecem intocados
  - **11.3** Distinções obrigatórias — 4 pares de termos com distinção normativa
  - **11.4** Ocupação integral do corpo e margens internas — 4 proibições
    explícitas para elementos que declaram `distribuicao_matricial`

### 3.6 contrato_lancador.md — Seção 11

**Arquivo:** `docs/contratos/contrato_lancador.md`

- Frontmatter `adrs_aplicadas`: adicionada ADR-0025
- Adicionada seção 11 com subseções 11.1 a 11.5:
  - **11.1** O que a ADR-0025 acrescenta — campo `distribuicao_matricial` opcional
  - **11.2** O que permanece — 6 políticas específicas do `lancador` intactas
  - **11.3** Precedência quando `distribuicao_matricial` está presente — tabela
    normativa de precedência sobre ADR-0001/0002/0003 (atualizado por
    PATCH_APLICACAO_ADR, DEC-APP-0025-02)
  - **11.4** H-0034 não corrigido — declaração explícita
  - **11.5** Fallback — `quadro mínimo de terminal pequeno`

### 3.7 contrato_json_dashboard.md — Seção 9

**Arquivo:** `docs/contratos/contrato_json_dashboard.md`

- Frontmatter `adrs_aplicadas`: adicionada ADR-0025
- Adicionada seção 9 com subseções 9.1 a 9.5:
  - **9.1** Localização do campo — exemplo JSON ilustrativo completo
  - **9.2** Vocabulário de campos — tabela de 26 caminhos de campo com tipos, condições e valores (critério: cada linha normativa de caminho, de `formacao.politica` até `alinhamento_interno.vertical`)
  - **9.3** Compatibilidade — sem migração, sem default estrutural
  - **9.4** Fallback — `quadro mínimo de terminal pequeno`
  - **9.5** Pendência de alinhamento do `dashboard` — explicitamente não resolvida

### 3.8 contrato_json_console.md — Seção 10

**Arquivo:** `docs/contratos/contrato_json_console.md`

- Frontmatter `adrs_aplicadas`: adicionada ADR-0025
- Adicionada seção 10 com subseções 10.1 a 10.5:
  - **10.1** Localização do campo — exemplo JSON ilustrativo completo
  - **10.2** Vocabulário de campos — remissão a `contrato_json_dashboard.md` seção 9.2
  - **10.3** Substituição de políticas geométricas quando `distribuicao_matricial`
    está presente — políticas substituídas e preservadas enumeradas nominalmente
    (atualizado por PATCH_APLICACAO_ADR, DEC-APP-0025-03)
  - **10.4** Compatibilidade — sem migração, sem default estrutural
  - **10.5** Fallback — `quadro mínimo de terminal pequeno`

### 3.9 contrato_json_lancador.md — Seção 9

**Arquivo:** `docs/contratos/contrato_json_lancador.md`

- Frontmatter `adrs_aplicadas`: adicionada ADR-0025
- Adicionada seção 9 com subseções 9.1 a 9.6:
  - **9.1** Localização do campo — exemplo JSON ilustrativo completo
  - **9.2** Vocabulário de campos — remissão a `contrato_json_dashboard.md` seção 9.2
  - **9.3** Compatibilidade — 5 políticas específicas preservadas quando ausente
  - **9.4** Mapeamento e sobreposições pendentes — tabela de 4 sobreposições não resolvidas
  - **9.5** Divergência do H-0034 — explicitamente não corrigida
  - **9.6** Fallback — `quadro mínimo de terminal pequeno`

---

## 4. Decisões tomadas durante APLICAR_ADR

### 4.1 Nome do campo no JSON do elemento

**Decisão:** `distribuicao_matricial`

**Justificativa:** A ADR-0025 deixou explicitamente o nome do campo para
APLICAR_ADR, solicitando verificação dos padrões documentais. Verificação
realizada:

- Campos de políticas existentes: `politica_composicao`, `politica_navegacao`,
  `politica_selecao`, `politica_paginacao`, `politica_exibicao` (console);
  `regras_exibicao` (lancador, dashboard)
- Campos de distribuição existentes: `distribuicao` (campo de alocação de área
  entre filhos de container estrutural)
- O nome `distribuicao` já está tomado com semântica distinta; `distribuicao_matricial`
  é composto que reflete o termo da própria ADR ("distribuição matricial
  configurável") sem colidir com o uso existente
- Mantém o padrão snake_case do projeto

### 4.2 Vocabulário de políticas de formação

**Decisão:** `"preferencia_linhas"`, `"preferencia_colunas"`, `"matriz_fixa"`

**Justificativa:** Nomes derivados diretamente do texto da ADR-0025 (seção 15),
traduzidos para snake_case conforme convenção do projeto. Sem alternativas
concorrentes não autorizadas.

### 4.3 Vocabulário de distribuição horizontal e vertical

**Decisão:**
- Horizontal: `"inicio"`, `"centro"`, `"fim"`, `"entre_participantes"`,
  `"uniforme"`, `"margens_limitadas"`
- Vertical: `"inicio"`, `"centro"`, `"fim"`, `"entre_linhas"`, `"uniforme"`,
  `"margens_limitadas"`

**Justificativa:** Derivados da semântica da ADR-0025 (seções 22 e 23). Os
nomes `"entre_participantes"` e `"entre_linhas"` refletem a assimetria
intencional entre eixos (ADR-0025 seção 17: os eixos são independentes).

### 4.4 Vocabulário de ordem de expansão

**Decisão:** `"margens_primeiro_depois_vaos"`, `"uniforme_margens_e_vaos"`,
`"vaos_primeiro_depois_margens"`

**Justificativa:** A ADR-0025 (seção 25) descreve três modelos de capacidade.
Os nomes aqui escolhidos descrevem a sequência de absorção do espaço excedente
de forma inequívoca. A ordem não está fixada como default universal — é
declarada por elemento.

### 4.5 Vocabulário de política de restos

**Decisão:** `"ao_primeiro"`, `"ao_ultimo"`

**Justificativa:** A ADR-0025 (seção 26) exige cardinalidade unitária e
resultado estável. As duas opções canônicas (primeiro ou último receptor recebe
a(s) unidade(s) residual(is)) são apresentadas como alternativas; a escolha é
feita por declaração explícita no JSON de cada elemento, sem default universal.

### 4.6 Vocabulário de dimensionamento

**Decisão:**
- Colunas: `"maior_da_coluna"`, `"uniforme"`, `"minimo_fixo"`
- Linhas: `"maior_da_linha"`, `"uniforme"`, `"minimo_fixo"`

**Justificativa:** Derivados da semântica da ADR-0025 (seção 20). Escolha
descritiva sem default universal; `"minimo_fixo"` requer campo `minimo` associado.

### 4.7 Vocabulário de alinhamento interno

**Decisão:**
- Horizontal: `"inicio"`, `"centro"`, `"fim"`
- Vertical: `"topo"`, `"centro"`, `"base"`

**Justificativa:** Derivados da semântica da ADR-0025 (seção 27). `"topo"` e
`"base"` em vez de `"inicio"` e `"fim"` no eixo vertical para clareza semântica.

### 4.8 Reconciliação terminológica (OBS-ADR0025-002)

**Decisão:** "terminal muito pequeno" = condição geométrica; `quadro mínimo de
terminal pequeno` = estado canônico exibido. Não são concorrentes.

**Implementação:** NOMENCLATURA.md seção 16.2 formaliza a distinção.

---

## 4 bis. Decisões complementares tomadas após QA (PATCH_APLICACAO_ADR)

As decisões desta seção não existiam durante APLICAR_ADR. Foram tomadas
explicitamente pelo usuário após o bloqueio identificado pelo QA
(RELATORIO_QA_APLICACAO_ADR-0025.md) e formalizadas nos contratos pelo
PATCH_APLICACAO_ADR. Elas são distintas das oito decisões originais da seção 4.

### DEC-APP-0025-01 — Tratamento interno do participante (QA-APP-ADR0025-BLOQ-001)

**Decisão:** `TRATAMENTO_INTERNO_DO_PARTICIPANTE`

Quando `dimensionamento.colunas.politica` ou `dimensionamento.linhas.politica`
for `"minimo_fixo"` e um participante exigir dimensão superior ao valor
declarado, a dimensão externa não cresce automaticamente. O participante trata
internamente seu conteúdo dentro da área recebida, com base nas autoridades
ativas (ADR-0025 seções 7 e 8; `contrato_composicao_corpo.md` seção 11.1; e
o contrato específico do elemento participante). A formação externa não se
torna inválida por exigência interna. A distribuição externa não reorganiza
descendentes. Nenhum truncamento, quebra, rolagem, paginação ou crescimento
externo automático é introduzido por este contrato.

**Implementação:** `contrato_json_dashboard.md` seção 9.2.1 (regra normativa);
herdada por remissão em `contrato_json_lancador.md` seção 9.2 e
`contrato_json_console.md` seção 10.2.

**Autoridade ativa de tratamento interno localizada:** ADR-0025 seções 7 e 8
(participante como unidade única no nível externo; distribuição interna é
responsabilidade própria) + `contrato_composicao_corpo.md` seção 11.1
(separação de responsabilidades entre composição hierárquica e distribuição
interna de participantes) + contrato específico de cada elemento participante.

### DEC-APP-0025-02 — Precedência no lançador (QA-APP-ADR0025-ALTO-001)

**Decisão:** `NOVA_CONFIGURACAO_TEM_PRECEDENCIA`

Quando o `lancador` declarar `distribuicao_matricial`, essa configuração tem
precedência sobre ADR-0001, ADR-0002 e ADR-0003 nas responsabilidades
sobrepostas (formação, distribuição horizontal, vãos, margens). Quando ausente,
todo o comportamento histórico permanece. H-0034 não é corrigido.

**Implementação:** `contrato_lancador.md` seção 11.3 (tabela normativa de
precedência); `contrato_json_lancador.md` seção 9.4 (tabela de campos e
precedência).

### DEC-APP-0025-03 — Substituição no console (QA-APP-ADR0025-ALTO-002)

**Decisão:** `NOVA_CONFIGURACAO_SUBSTITUI_POLITICAS_RELACIONADAS`

Quando o `console` declarar `distribuicao_matricial`, as políticas existentes
relacionadas à organização geométrica do conteúdo são integralmente
substituídas. Quando ausente, todas as políticas anteriores permanecem. Políticas
funcionais não geométricas são preservadas em ambos os casos.

**Implementação:** `contrato_json_console.md` seção 10.3 (políticas substituídas
e preservadas enumeradas nominalmente).

---

## 5. Itens deliberadamente não fechados durante APLICAR_ADR

Os seguintes itens foram identificados durante APLICAR_ADR e registrados nos
contratos como pendências explícitas. Três foram resolvidos pelo
PATCH_APLICACAO_ADR (DEC-APP-0025-01, DEC-APP-0025-02, DEC-APP-0025-03); dois
permanecem como pendências futuras não bloqueantes.

| Item | Localização original | Status após patch |
|---|---|---|
| Reconciliação entre `distribuicao_matricial` e ADR-0001/0002/0003 no `lancador` | `contrato_lancador.md` seção 11.3; `contrato_json_lancador.md` seção 9.4 | **Resolvida** — DEC-APP-0025-02: precedência formalizada com tabela normativa |
| Divergência geométrica do H-0034 | `contrato_lancador.md` seção 11.4; `contrato_json_lancador.md` seção 9.5 | **Pendente** — futuro não bloqueante; ciclo documental próprio |
| Alinhamento horizontal do `dashboard` (centralizado vs. bloco à esquerda) | `contrato_json_dashboard.md` seção 9.5 | **Pendente** — futuro não bloqueante; pré-existente à ADR-0025 |
| Comportamento quando participante excede dimensão `minimo_fixo` | `contrato_json_dashboard.md` seção 9.2 | **Resolvida** — DEC-APP-0025-01: tratamento interno do participante formalizado em seção 9.2.1 |
| Reconciliação entre `distribuicao_matricial` e políticas específicas do `console` | `contrato_json_console.md` seção 10.3 | **Resolvida** — DEC-APP-0025-03: substituição integral de políticas geométricas formalizada |

---

## 6. Verificação de integridade (21 pontos)

- [x] **1.** Status da ADR-0025 atualizado no frontmatter (`aceita e aplicada`)
- [x] **2.** Status da ADR-0025 atualizado na tabela da seção 1 (`aceita e aplicada`)
- [x] **3.** Status da ADR-0025 atualizado na seção 2 (`aceita e aplicada`)
- [x] **4.** Decisões da ADR-0025 não alteradas
- [x] **5.** INDICE_ADR.md — entrada ADR-0025 adicionada com status `aceita e aplicada`
- [x] **6.** NOMENCLATURA.md — seção 16 adicionada com terminologia canônica
- [x] **7.** OBS-ADR0025-002 resolvida — "terminal muito pequeno" vs. `quadro mínimo de terminal pequeno` reconciliados em NOMENCLATURA.md seção 16.2
- [x] **8.** `contrato_tela_json.md` — seção 30 adicionada; frontmatter atualizado
- [x] **9.** `contrato_composicao_corpo.md` — seção 11 adicionada; frontmatter atualizado
- [x] **10.** `contrato_lancador.md` — seção 11 adicionada; frontmatter atualizado
- [x] **11.** `contrato_json_dashboard.md` — seção 9 adicionada; frontmatter atualizado
- [x] **12.** `contrato_json_console.md` — seção 10 adicionada; frontmatter atualizado
- [x] **13.** `contrato_json_lancador.md` — seção 9 adicionada; frontmatter atualizado
- [x] **14.** Campo `distribuicao_matricial` formalizado nos três elementos com vocabulário completo
- [x] **15.** Escopo de nível único explícito em todos os documentos relevantes (sem recursão, cascata, herança, multinível)
- [x] **16.** Compatibilidade com JSONs existentes declarada em todos os contratos (sem migração automática, sem default estrutural)
- [x] **17.** Fallback usa `quadro mínimo de terminal pequeno` (não "terminal muito pequeno") em todos os contratos
- [x] **18.** ADR-0001/0002/0003 do `lancador` preservadas quando `distribuicao_matricial` está ausente; precedência formalizada por DEC-APP-0025-02 quando presente
- [x] **19.** H-0034 não corrigido — declaração explícita em dois documentos
- [x] **20.** Paginação excluída explicitamente em `contrato_tela_json.md` seção 30.6 e nos contratos JSON
- [x] **21.** ADR-0024 (preenchimento externo proibido) não violada — distinção entre margem interna e espaço externo indevido estabelecida em `contrato_composicao_corpo.md` seção 11.4 e `contrato_tela_json.md` seção 30.4

---

## 7. Arquivos alterados

### 7.1 Alterações da APLICAR_ADR original

| Arquivo | Tipo de alteração | Observação Git |
|---|---|---|
| `docs/adr/ADR-0025-...md` | Status atualizado (frontmatter + seção 1 + seção 2) | Não rastreado — arquivo preexistente fora do índice Git; ausência em `git diff --name-only` não implica ausência de conteúdo |
| `docs/adr/INDICE_ADR.md` | Linha ADR-0025 adicionada | Rastreado modificado |
| `docs/NOMENCLATURA.md` | Seção 16 adicionada (5 subseções) | Rastreado modificado |
| `docs/contratos/contrato_tela_json.md` | Frontmatter + seção 30 adicionados | Rastreado modificado |
| `docs/contratos/contrato_composicao_corpo.md` | Frontmatter + seção 11 adicionados | Rastreado modificado |
| `docs/contratos/contrato_lancador.md` | Frontmatter + seção 11 adicionados | Rastreado modificado |
| `docs/contratos/contrato_json_dashboard.md` | Frontmatter + seção 9 adicionados | Rastreado modificado |
| `docs/contratos/contrato_json_console.md` | Frontmatter + seção 10 adicionados | Rastreado modificado |
| `docs/contratos/contrato_json_lancador.md` | Frontmatter + seção 9 adicionados | Rastreado modificado |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md` | Criado (este arquivo) | Não rastreado — criado neste ciclo |

O `git diff --name-only` registra 8 arquivos rastreados modificados. A ADR-0025
é não rastreada, portanto não aparece no diff rastreado, mas teve seu conteúdo
alterado durante APLICAR_ADR. Os 8 arquivos rastreados modificados são:
`INDICE_ADR.md`, `NOMENCLATURA.md`, `contrato_tela_json.md`,
`contrato_composicao_corpo.md`, `contrato_lancador.md`,
`contrato_json_dashboard.md`, `contrato_json_console.md`,
`contrato_json_lancador.md`. O relatório de aplicação foi criado durante a
etapa; os relatórios QA de entrada são preexistentes e não produzidos pela
aplicação.

### 7.2 Alterações do PATCH_APLICACAO_ADR

| Arquivo | Tipo de alteração |
|---|---|
| `docs/contratos/contrato_json_dashboard.md` | Seção 9.2.1 adicionada (DEC-APP-0025-01) |
| `docs/contratos/contrato_lancador.md` | Seção 11.3 substituída por tabela normativa de precedência (DEC-APP-0025-02) |
| `docs/contratos/contrato_json_lancador.md` | Seção 9.2 atualizada com remissão a 9.2.1; seção 9.4 substituída por precedência resolvida (DEC-APP-0025-02) |
| `docs/contratos/contrato_json_console.md` | Seção 10.2 atualizada com remissão a 9.2.1; seção 10.3 substituída por substituição de políticas geométricas (DEC-APP-0025-03) |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md` | Múltiplas correções factuais (QA-APP-ADR0025-MEDIO-001, BAIXO-001, BAIXO-002) |

**Arquivos não alterados (como exigido):**
- `docs/relatorios/RELATORIO_QA_ADR-0025.md` — intocado
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md` — intocado
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md` — intocado
- `docs/adr/ADR-0025-...md` — intocado neste patch
- `docs/NOMENCLATURA.md` — intocado neste patch
- `docs/contratos/contrato_tela_json.md` — intocado neste patch
- `docs/contratos/contrato_composicao_corpo.md` — intocado neste patch
- Quaisquer outros ADRs
- `config/`, `demo/`, `tela/` — intocados
- Código, testes — intocados

---

## 8. Resumo do ciclo

```yaml
ciclo: APLICAR_ADR
adr: ADR-0025
status_entrada: ADR_APPROVED_WITH_NOTES
status_saida: APLICACAO_CONCLUIDA
estado_da_aplicacao:
  arquivos_rastreados_modificados: 8
  arquivo_nao_rastreado_preexistente_alterado:
    - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  arquivo_criado_pela_aplicacao:
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  relatorios_qa_preexistentes_preservados:
    - docs/relatorios/RELATORIO_QA_ADR-0025.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
decisoes_semanticas_da_aplicacao_original: 8
decisoes_editoriais_confirmadas: 0
decisoes_semanticas_pos_qa:
  - DEC-APP-0025-01
  - DEC-APP-0025-02
  - DEC-APP-0025-03
total_de_decisoes_semanticas_documentadas: 11
pendencias_mantidas: 2
pendencias_mantidas_lista:
  - divergencia_h_0034
  - alinhamento_horizontal_dashboard
pendencias_resolvidas:
  - OBS-ADR0025-002 (reconciliacao terminologica)
  - comportamento_minimo_fixo_excedido (DEC-APP-0025-01)
  - reconciliacao_lancador_adr_0001_0002_0003 (DEC-APP-0025-02)
  - reconciliacao_console_politicas_especificas (DEC-APP-0025-03)
proxima_categoria: null
observacoes:
  - Nenhum BLOCKED_USER_DECISION foi acionado durante APLICAR_ADR
  - Nenhum BLOCKED_DOCUMENTATION foi acionado durante APLICAR_ADR
  - Nenhum ARCHITECTURE_REVIEW_REQUIRED foi acionado durante APLICAR_ADR
  - OBS-ADR0025-POS-001 nao requereu alteracao documental
  - PATCH_APLICACAO_ADR concluido em 2026-07-16 com 3 decisoes complementares do usuario
```
