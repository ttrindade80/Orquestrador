---
name: RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA
description: Auditoria documental independente pós-patch da ADR-0028 — revisão de modos por tela. Verifica correção de QA-MODOS-001 e QA-MODOS-002, preservação de QA-MODOS-003 e QA-MODOS-004, ausência de regressões e fidelidade à decisão do usuário.
metadata:
  type: relatorio_qa_pos_patch_revisao_modos_por_tela
  adr_auditada: ADR-0028
  qa_de_origem: docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md
  data: "2026-07-17"
  auditor: independente (contexto limpo)
  status_literal: ADR_APPROVED_WITH_NOTES
---

# Relatório de QA Pós-Patch — ADR-0028: Revisão de Modos por Tela

---

## 1. Identificação

| Campo | Valor |
|---|---|
| Relatório | `RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md` |
| ADR auditada | `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` |
| QA de origem | `docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md` |
| Data | 2026-07-17 |
| Ciclo precedente | PATCH_ADR (correção de QA-MODOS-001 e QA-MODOS-002) |
| Status recebido | `ADR_PATCHED` |
| Status de origem | `ADR_REJECTED` |

---

## 2. Objetivo

Auditar de forma independente a ADR-0028 no estado pós-patch (correção de QA-MODOS-001 e QA-MODOS-002) para determinar se:

1. `QA-MODOS-001` foi integralmente corrigido;
2. `QA-MODOS-002` foi integralmente corrigido;
3. as observações `QA-MODOS-003` e `QA-MODOS-004` permanecem corretamente preservadas;
4. o patch não introduziu regressões normativas, terminológicas ou de escopo;
5. as três políticas de modo estão normativamente distintas;
6. a regra de ausência de configuração está corretamente estruturada;
7. os quatro cenários mínimos permanecem íntegros;
8. nenhuma decisão nova foi inventada;
9. a ADR revisada está pronta para nova aplicação documental.

**Proibições absolutas desta auditoria:** corrigir a ADR; alterar contratos; alterar o handoff H-0037; implementar qualquer funcionalidade; preparar stage ou commit; iniciar outro ciclo.

---

## 3. Autoridades

| Documento | Papel nesta Auditoria |
|---|---|
| Decisão funcional vigente (§7 do prompt) | Autoridade suprema — prevalece sobre relatórios anteriores |
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | Documento auditado (lido integralmente) |
| `docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md` | QA de origem — fonte dos achados corretivos |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` | Histórico — referência para preservações |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md` | Histórico — referência focal |
| `docs/contratos/contrato_json_console.md` | Referência focal — estado pré-D23 esperado |
| `docs/contratos/contrato_console.md` | Referência focal — estado pré-D23 esperado |
| `docs/contratos/contrato_barra_de_menus.md` | Referência focal — estado pré-D23 esperado |
| `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` | Referência focal — avaliação de impacto |
| `docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md` | Histórico — aprovação anterior não vale após D23 |

---

## 4. Estado Git

```yaml
branch: master
head: f6982d0
git_diff_check: LIMPO (DIFF_CHECK_OK)
stage: VAZIO

arquivos_modificados_rastreados_M:
  - docs/NOMENCLATURA.md              # acumulado APLICAR_ADR (D1–D22)
  - docs/adr/INDICE_ADR.md            # acumulado APLICAR_ADR (D1–D22)
  - docs/contratos/contrato_barra_de_menus.md    # acumulado APLICAR_ADR (D1–D22)
  - docs/contratos/contrato_composicao_corpo.md  # acumulado APLICAR_ADR (D1–D22)
  - docs/contratos/contrato_console.md           # acumulado APLICAR_ADR (D1–D22)
  - docs/contratos/contrato_json_console.md      # acumulado APLICAR_ADR (D1–D22)
  - docs/contratos/contrato_tela_json.md         # acumulado APLICAR_ADR (D1–D22)

arquivos_nao_rastreados_nova_criacao:
  - docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
  - docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md

arquivos_nao_rastreados_nao_documentais:
  - demo/__pycache__/     # artefato Python auto-gerado, fora do escopo
  - tela/__pycache__/     # artefato Python auto-gerado, fora do escopo
```

**Confirmação do escopo do patch:** o patch QA-MODOS alterou somente a ADR-0028. Os sete arquivos em `M` decorrem de etapas anteriores autorizadas (APLICAR_ADR D1–D22) e permanecem inalterados pelo patch. Os `__pycache__` são artefatos Python sem relevância documental. Nenhum arquivo inesperado com origem documental não confirmada foi identificado.

---

## 5. QA de Origem

O `RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md` (status `ADR_REJECTED`) identificou:

**Achados corretivos:**

| ID | Seção | Severidade | Natureza | Exige decisão do usuário |
|---|---|---|---|---|
| QA-MODOS-001 | §36.3 | médio | corretivo | não |
| QA-MODOS-002 | D23, §43 item 3, §39 | baixo | corretivo | não |

**Observações não corretivas:**

| ID | Seção | Severidade | Natureza |
|---|---|---|---|
| QA-MODOS-003 | §36.2 cenário 3, §43 item 3 | observação | não corretivo |
| QA-MODOS-004 | contratos e H-0037 | observação | não corretivo |

---

## 6. Patch Recebido

O `§47 — Histórico de alterações` da ADR-0028 registra a última entrada:

> Correção pós-QA da revisão de modos por tela (PATCH_ADR): (1) §36.3 — definição do escopo de medição de alinhamento no cenário verboso de dois níveis: conteúdo lógico completo do cenário, coluna comum estável entre páginas, continuação do segundo nível alinhada à mesma coluna inicial, sem largura fixa global (QA-MODOS-001); (2) D23, §25, §39 e §43 item 3 — distinção explícita entre telas novas ou revisadas (política obrigatória, ausência inválida, default implícito proibido) e telas legadas (compatibilidade preservada, reinterpretação automática proibida, migração adiada); §44 e §45 atualizados com critério de distinção; §46 atualizado com verificações 27–34 (QA-MODOS-002). A aplicação documental anterior (D1–D22) precisará ser revisada para incorporar D23 quando a ADR for aprovada.

A declaração mapeia exatamente sobre QA-MODOS-001 e QA-MODOS-002. O patch declara ainda que `schema_concreto_inventado: false` e `conteudo_matricial_reintroduzido: false`, consistente com os achados de regressão a seguir.

---

## 7. Verificação de QA-MODOS-001

### 7.1 Achado original

§36.3 não especificava o escopo da medição do "maior texto do nível 1" para a regra de alinhamento do cenário de dois níveis em modo verboso. Sem escopo declarado, implementadores distintos poderiam escolher escopos diferentes (irmãos, grupo, nível, página, conteúdo completo) e produzir colunas de alinhamento incompatíveis com os mesmos dados — violando o Determinismo declarado em §13.6.

### 7.2 Texto de §36.3 no estado auditado

```text
No cenário de tela somente verbosa com conteúdo de dois níveis (cenário 2 de §36.2), a largura
de referência para alinhamento deve ser calculada considerando todos os textos identificadores
do primeiro nível pertencentes ao conteúdo lógico completo do cenário.

A maior largura encontrada entre esses textos determina a coluna comum a partir da qual o
conteúdo do segundo nível deve iniciar. Essa coluna deve permanecer estável entre páginas:
paginação e repetição visual de contexto não alteram o resultado da medição. As linhas de
continuação do conteúdo do segundo nível devem permanecer alinhadas à mesma coluna inicial.

A medição usa o escopo `conteúdo completo` definido em §27, restrito ao conteúdo lógico do
cenário. Ela não estabelece largura fixa global para outras telas ou outros cenários.
```

### 7.3 Verificações obrigatórias

| # | Verificação | Resultado |
|---|---|---|
| 1 | Todos os identificadores de primeiro nível do conteúdo lógico completo participam da medição | CONFIRMADO — "todos os textos identificadores do primeiro nível pertencentes ao conteúdo lógico completo do cenário" |
| 2 | A maior largura determina uma coluna comum | CONFIRMADO — "A maior largura encontrada entre esses textos determina a coluna comum" |
| 3 | Todos os conteúdos de segundo nível começam nessa coluna | CONFIRMADO — "a partir da qual o conteúdo do segundo nível deve iniciar" |
| 4 | Linhas de continuação usam a mesma coluna | CONFIRMADO — "As linhas de continuação do conteúdo do segundo nível devem permanecer alinhadas à mesma coluna inicial" |
| 5 | Paginação não recalcula a medida | CONFIRMADO — "paginação e repetição visual de contexto não alteram o resultado da medição" |
| 6 | Repetição visual de contexto não altera a medida | CONFIRMADO — explicitamente declarado na mesma cláusula do item anterior |
| 7 | A regra não cria largura fixa global | CONFIRMADO — "Ela não estabelece largura fixa global para outras telas ou outros cenários" |
| 8a | A regra não foi generalizada para tabela | CONFIRMADO — escopo restrito a "cenário 2 de §36.2" (tela somente verbosa de dois níveis) |
| 8b | A regra não foi generalizada para cenário de três níveis | CONFIRMADO — escopo restrito; cenário 3 de §36.2 não é abrangido |
| 8c | A regra não foi generalizada para todas as hierarquias | CONFIRMADO — vocabulário "do cenário" restringe ao conteúdo lógico deste cenário específico |
| 8d | A regra não foi generalizada para outras telas | CONFIRMADO — "Ela não estabelece largura fixa global para outras telas ou outros cenários" |
| 9 | A redação é determinística sem inventar algoritmo físico não autorizado | CONFIRMADO — a medição usa o escopo `conteúdo completo` já definido em §27; nenhum algoritmo novo foi inventado |

**Verificações de §46 (integridade):**

As verificações 25, 27, 28 e 29 de §46 confirmam:
- 25: §36.3 existe — "Confirmado"
- 27: "Escopo da medição de alinhamento em §36.3 definido como conteúdo lógico completo do cenário — Confirmado"
- 28: "Coluna do segundo nível estável entre páginas — paginação não altera a medição — Confirmado"
- 29: "Linhas de continuação do segundo nível alinhadas à mesma coluna inicial — Confirmado"

### 7.4 Classificação

```text
CORRIGIDO
```

A regra de alinhamento agora é determinística: o escopo é `conteúdo completo` (§27) restrito ao conteúdo lógico do cenário; a coluna é calculada uma vez e permanece estável entre páginas; a continuação usa a mesma coluna; a regra não é generalizada. Dois implementadores com os mesmos dados produzirão a mesma geometria.

---

## 8. Verificação de QA-MODOS-002

### 8.1 Achado original

D23 usava obrigação universal ("Cada tela de console multinível deve declarar sua política de modo de apresentação") sem distinguir explicitamente telas novas ou revisadas de telas legadas anteriores a D23. Isso criava tensão com §39 (que declarava as fixtures H-0036 como válidas) e com §43 item 3 (que pressupunha telas sem declaração).

### 8.2 Texto das seções relevantes no estado auditado

**D23 — Escopo de aplicação explícito (trecho):**

```text
Escopo de aplicação de D23 — telas novas ou revisadas e telas legadas

A obrigação declarativa de D23 aplica-se a telas novas ou revisadas para adotar a capacidade
definida por esta ADR:
- omitir a política é inválido para essas telas;
- uma tela alternável deve declarar também o modo inicial;
- não existe default implícito que substitua a declaração obrigatória.

Telas criadas antes da incorporação de D23 — como as do ciclo H-0036, usado aqui apenas como
exemplo histórico de tela legada — permanecem válidas segundo os contratos vigentes no momento
de sua criação:
- não devem ser reinterpretadas automaticamente como uma das três políticas;
- não recebem campo, valor ou default por inferência;
- não precisam ser migradas por esta ADR;
- continuam sujeitas a futura decisão de migração e compatibilidade.
```

**§25 — Modo inicial (trecho final):**

```text
Esta obrigação aplica-se a telas novas ou revisadas conforme o escopo de D23. Telas legadas —
criadas antes da incorporação de D23 — não precisam declarar modo inicial até futura decisão
de migração.
```

**§39 — H-0036 (trecho):**

```text
O ciclo H-0036 pré-data a incorporação de D23; suas telas não declaram política de modo e não
devem ser reinterpretadas automaticamente como uma das três políticas. Migração futura permanece
adiada conforme §43 item 3.
```

**§43 item 3 (trecho relevante da nota parentética):**

```text
...estratégia de migração das telas legadas e eventual representação de compatibilidade no
loader (para telas novas ou revisadas, política ausente é inválida e default implícito é
proibido; para telas legadas, política ausente é compatibilidade preservada e interpretação
automática é proibida)
```

### 8.3 Verificações obrigatórias

| # | Verificação | Resultado |
|---|---|---|
| 1 | D23 identifica seu escopo de aplicação | CONFIRMADO — "Escopo de aplicação de D23 — telas novas ou revisadas e telas legadas" |
| 2 | Telas novas ou revisadas devem declarar política | CONFIRMADO — "aplica-se a telas novas ou revisadas para adotar a capacidade definida por esta ADR" |
| 3 | A ausência é inválida para essas telas | CONFIRMADO — "omitir a política é inválido para essas telas" |
| 4 | Não existe default implícito para telas novas ou revisadas | CONFIRMADO — "não existe default implícito que substitua a declaração obrigatória" |
| 5 | Telas alternáveis declaram modo inicial | CONFIRMADO — "uma tela alternável deve declarar também o modo inicial" (em D23) e §25 |
| 6 | Telas legadas permanecem válidas | CONFIRMADO — "permanecem válidas segundo os contratos vigentes no momento de sua criação" |
| 7 | Telas legadas não são reinterpretadas automaticamente | CONFIRMADO — "não devem ser reinterpretadas automaticamente como uma das três políticas" |
| 8 | H-0036 aparece apenas como exemplo histórico, não como exceção exclusiva | CONFIRMADO — "como as do ciclo H-0036, usado aqui apenas como exemplo histórico de tela legada" |
| 9 | A ADR não atribui uma das três políticas às telas legadas por inferência | CONFIRMADO — "não recebem campo, valor ou default por inferência" |
| 10 | A estratégia de migração continua adiada | CONFIRMADO — "continuam sujeitas a futura decisão de migração e compatibilidade" e §43 item 3 |
| 11a | §25 é coerente com D23 | CONFIRMADO — §25 aplica a mesma distinção: obrigação para telas novas ou revisadas; telas legadas aguardam futura decisão |
| 11b | §39 é coerente com D23 | CONFIRMADO — §39 trata H-0036 como legado pré-D23, sem reinterpretação automática, migração adiada |
| 11c | §43 é coerente com D23 | CONFIRMADO — parentético de §43 item 3 é preciso: ausência inválida para novas, compatibilidade preservada para legadas |
| 11d | §44 é coerente com D23 | CONFIRMADO — §44 inclui "distinguir explicitamente telas novas ou revisadas — que exigem declaração de política — de telas legadas que permanecem válidas sem declaração" |
| 11e | §45 é coerente com D23 | CONFIRMADO — §45 inclui "respeitar a distinção entre telas novas ou revisadas com política declarada e telas legadas sem declaração — telas legadas não recebem política por inferência" |
| 11f | §46 é coerente com D23 | CONFIRMADO — verificações 30–34 de §46 confirmam explicitamente a distinção e seus efeitos |

**Verificações de §46 (integridade), verificações 30–34:**

- 30: "D23 distingue telas novas ou revisadas (política obrigatória) de telas legadas (compatibilidade preservada) — Confirmado"
- 31: "Telas legadas permanecem válidas sem declaração de política — Confirmado"
- 32: "Telas legadas não são reinterpretadas automaticamente como uma das três políticas — Confirmado"
- 33: "Migração de telas legadas permanece adiada — Confirmado"
- 34: "Ausência de política é inválida somente para telas novas ou revisadas; default implícito é proibido — Confirmado"

### 8.4 Verificação adicional — §43 item 3 e "valores padrão quando ausente"

O QA de origem apontou que a formulação "valores padrão quando configuração estiver ausente" em §43 item 3 poderia ser lida como abrindo default implícito para telas novas. A versão auditada substitui essa formulação por uma nota parentética que distingue explicitamente os dois casos: para telas novas ou revisadas, política ausente é inválida e default implícito é proibido; para telas legadas, política ausente é compatibilidade preservada. A tensão foi resolvida sem criar nova política.

### 8.5 Classificação

```text
CORRIGIDO
```

A distinção entre telas novas ou revisadas e telas legadas está agora explícita em D23, §25, §39, §43 item 3, §44, §45 e §46. As seis seções são coerentes entre si. A tensão identificada no QA de origem foi eliminada.

---

## 9. Tratamento de QA-MODOS-003

### 9.1 Observação original

O cenário 3 de §36.2 (tela alternável de três níveis, iniciando em modo não verboso) exige que o schema permita declarar modo inicial não verboso. O único valor de schema estabelecido era `excesso.modo: "verboso"`. A ADR não havia inventado campos ou valores concretos; registrava implicitamente a dependência do schema em §43 item 3.

### 9.2 Verificações

| # | Verificação | Resultado |
|---|---|---|
| 1 | A ADR mantém o cenário alternável iniciando não verboso | CONFIRMADO — §36.2 cenário 3: "Tela alternável de três níveis — iniciando em modo não verboso" |
| 2 | A ADR não inventou propriedades ou valores concretos de schema | CONFIRMADO — §43 item 3 permanece com nomes de campos e valores adiados |
| 3 | A ADR identifica que a aplicação documental posterior definirá a representação concreta | CONFIRMADO — §43 item 3: "mecanismo concreto de schema adiado" |
| 4 | A ADR não trata a insuficiência atual dos contratos como defeito da decisão conceitual | CONFIRMADO — §43 item 3 trata isso como decisão pendente de etapa futura |

### 9.3 Classificação

```text
OBSERVACAO_PRESERVADA
```

A observação permanece válida: o cenário 3 não pode ser demonstrado com o schema atual (apenas `excesso.modo: "verboso"` existe como valor estabelecido). O conceito está decidido (D23(c), §25); o mecanismo concreto de schema permanece corretamente adiado. Esta limitação não bloqueia a aprovação da ADR.

---

## 10. Tratamento de QA-MODOS-004

### 10.1 Observação original

A aplicação documental anterior propagou D1–D22 antes da existência de D23. Os contratos resultantes apresentam divergências em relação a D23: chip `[V] Verboso` sem restrição a alternáveis; ausência das três políticas de modo; `contrato_json_console.md §13.11` incompatível com telas de modo único.

### 10.2 Verificações

| # | Verificação | Resultado |
|---|---|---|
| 1 | Os contratos atuais permanecem anteriores a D23 | CONFIRMADO — git status mostra os contratos em estado `M` (modificados pela aplicação D1–D22, não pelo patch QA-MODOS) |
| 2 | A ADR registra que os contratos precisam de reaplicação | CONFIRMADO — §47 última entrada: "A aplicação documental anterior (D1–D22) precisará ser revisada para incorporar D23 quando a ADR for aprovada" |
| 3 | Os contratos não foram alterados durante o patch QA-MODOS | CONFIRMADO — nenhum arquivo de contrato foi modificado pelo patch; o git status de contratos reflete apenas o estado anterior (APLICAR_ADR D1–D22) |
| 4 | O H-0037 permanece bloqueado operacionalmente | CONFIRMADO — o QA de origem declarou `BLOQUEADO_POR_MUDANCA_DOCUMENTAL`; a causa (D23 não propagada aos contratos) permanece |
| 5 | A implementação não foi liberada | CONFIRMADO — nenhuma alteração de código ou configuração foi introduzida |

### 10.3 Classificação

```text
OBSERVACAO_PRESERVADA
```

As divergências entre contratos e D23 são esperadas e serão resolvidas pela futura re-aplicação documental incorporando D23. Não constituem defeito da ADR pós-patch.

---

## 11. Políticas de Tela

### 11.1 Somente verbosa

| Comportamento | Texto auditado | Resultado |
|---|---|---|
| Abre verbosa | D23(a): "a tela sempre abre em modo verboso" | CONFIRMADO |
| Permanece verbosa (não alterna) | D23(a): "não há alternância por V" | CONFIRMADO |
| Tecla V não aplicável | D11: "Em telas de modo único, a tecla V não é ação aplicável" | CONFIRMADO |
| Chip não obrigatório | D23(a): "o chip [V] Verboso não é obrigatório" | CONFIRMADO |

### 11.2 Somente não verbosa

| Comportamento | Texto auditado | Resultado |
|---|---|---|
| Abre não verbosa | D23(b): "a tela sempre abre em modo não verboso" | CONFIRMADO |
| Permanece não verbosa (não alterna) | D23(b): "não há alternância por V" | CONFIRMADO |
| Tecla V não aplicável | D11 | CONFIRMADO |
| Chip não obrigatório | D23(b): "o chip [V] Verboso não é obrigatório" | CONFIRMADO |
| Truncamento com `...` válido | D23(b): "truncamento com ... permanece válido quando aplicável" | CONFIRMADO |

### 11.3 Alternável

| Comportamento | Texto auditado | Resultado |
|---|---|---|
| Admite dois modos | D23(c): "a tela suporta os dois modos" | CONFIRMADO |
| Chip obrigatório | D23(c): "o chip [V] Verboso é obrigatório" / §23 | CONFIRMADO |
| `V` alterna | D23(c) e D11 | CONFIRMADO |
| Modo inicial obrigatório | D23(c): "a tela deve declarar o modo inicial" / D12 / §25 | CONFIRMADO |
| Início verboso ou não verboso | D23(c): "que pode ser verboso ou não verboso" | CONFIRMADO |
| Segunda ativação restaura estado anterior | D11: "uma segunda ativação deve retornar ao modo anterior" | CONFIRMADO |
| Alternância reversível | D23(c) e D11 | CONFIRMADO |

As três políticas são normativamente distintas e não se sobrepõem.

---

## 12. Ausência de Configuração

### 12.1 Telas novas ou revisadas

```yaml
politica_ausente: invalida
default_implicito: proibido
```

Confirmado em D23 escopo ("omitir a política é inválido para essas telas"; "não existe default implícito que substitua a declaração obrigatória") e em §43 item 3 parentético.

### 12.2 Telas legadas

```yaml
validade_anterior: preservada
reinterpretacao_automatica: proibida
default_por_inferencia: proibido
migracao_imediata: nao_exigida
```

Confirmado em D23 escopo, §25, §39, §43 item 3, §44, §45.

### 12.3 Avaliação de "valores padrão quando ausente"

A formulação original de §43 item 3 era: *"valores padrão quando configuração estiver ausente"*. Na versão auditada, esse trecho foi substituído por nota parentética que distingue explicitamente: para novas, política ausente é inválida e default é proibido; para legadas, política ausente é compatibilidade preservada. A expressão deixou de ser ambiguamente ampla. Não há mais risco de interpretação que permita default implícito para telas novas abrangidas por D23.

---

## 13. Schema Concreto

### 13.1 Suficiência para a próxima aplicação documental

```text
INSUFICIENTE_MAS_APLICAVEL_SEM_NOVA_DECISAO
```

**Justificativa:**

A ADR decidiu conceitualmente:
- as três classes de política (D23);
- a obrigação de declarar modo inicial em telas alternáveis (D12, §25);
- que o modo inicial pode ser verboso ou não verboso (D23(c));
- que telas legadas não recebem inferência (D23 escopo).

O que não foi decidido (§43 item 3):
- o nome concreto do campo para declarar a política da tela;
- os valores concretos aceitos por esse campo;
- o nome concreto do campo para declarar o modo inicial em telas alternáveis;
- o valor concreto para "modo inicial não verboso".

Esses itens são nomes e valores de schema, não escolhas comportamentais. A decisão funcional de D23 é suficiente para os contratos definirem a forma concreta sem precisar escolher comportamento novo. A re-aplicação documental pode formular os campos e valores a partir de D23 sem novas decisões arquiteturais.

**Nota sobre `excesso.modo: "verboso"`:** o único valor estabelecido atualmente representa "modo inicial verboso" em telas alternáveis (cenário 4 de §36.2). Sozinho, não representa as políticas somente verbosa, somente não verbosa, alternável nem o modo inicial não verboso. O schema precisa de extensão, que pode ser decidida na aplicação documental.

---

## 14. Quatro Cenários Mínimos

| Cenário | Política | Modo inicial | Chip | Tecla V | Resultado |
|---|---|---|---|---|---|
| 1 — somente não verbosa com truncamento `...` | somente não verbosa | não verboso (único) | não | não | PRESENTE |
| 2 — somente verbosa com dois níveis e múltiplas linhas | somente verbosa | verboso (único) | não | não | PRESENTE |
| 3 — alternável de três níveis iniciando não verbosa | alternável | não verboso (declarado) | sim | sim | PRESENTE |
| 4 — tabela alternável iniciando verbosa | alternável | verboso (declarado) | sim | sim | PRESENTE |

**Verificações adicionais:**

| Verificação | Resultado |
|---|---|
| Os cenários são tipos mínimos futuros (não definem profundidade máxima global) | CONFIRMADO — "cenários mínimos" em §36.2; §20.3 e §15.4 proíbem profundidade inferida |
| Os cenários não introduzem conteúdo matricial | CONFIRMADO — §42 exclui `tipo: matriz`; §6 restringe escopo ao console com conteúdo multinível |
| Os cenários não generalizam a política para outros componentes | CONFIRMADO — §6 e §42 confirmam exclusão de dashboard, lancador e outros componentes |

---

## 15. Ausência de Regressão

### 15.1 Escopo

| Verificação | Resultado |
|---|---|
| Escopo exclusivo de console multinível | CONFIRMADO — §6 |
| Sem conteúdo matricial | CONFIRMADO — §6, §42, §46 verificação 2 |
| Sem generalização para dashboard, lancador ou outros | CONFIRMADO — §42 |

### 15.2 Origem dos dados

| Verificação | Resultado |
|---|---|
| Origem atual por JSON externo | CONFIRMADO — §7 |
| Futura origem pelo Pipeline sem protocolo concreto | CONFIRMADO — §8, §43 itens 10–15 |
| Fronteira semântica estável em JSON | CONFIRMADO — §9 |
| Separação entre estrutura e conteúdo | CONFIRMADO — D1, D3, §9 |
| Carregamento separado | CONFIRMADO — D3, §35.1 |
| Entrega conjunta (sem fusão) | CONFIRMADO — D3, §35.1 |

### 15.3 Apresentações e modos

| Verificação | Resultado |
|---|---|
| Tabela | CONFIRMADO — D15, §17 |
| Hierarquia | CONFIRMADO — D16, §18 |
| Conjuntos e campos (2 níveis) | CONFIRMADO — D17, §19 |
| Conjuntos, subconjuntos e campos (3 níveis) | CONFIRMADO — D17, §20 |
| Modo não verboso | CONFIRMADO — D9, §21 |
| Modo verboso | CONFIRMADO — D10, §22 |
| Alternância reversível | CONFIRMADO — D11, §23 |
| Não persistência | CONFIRMADO — §24 |
| Paginação | CONFIRMADO — §30 |
| Impossibilidade geométrica | CONFIRMADO — §32 |

### 15.4 Responsabilidades e validação

| Verificação | Resultado |
|---|---|
| Responsabilidades das camadas | CONFIRMADO — §35 (ponto de entrada, loader, modelo, renderizador) |
| Validação manual em TTY real | CONFIRMADO — §38 |
| Validações V-01 a V-15 | CONFIRMADO — §33; nenhuma validação alterada ou removida pelo patch |

### 15.5 Decisões D1–D22

Nenhuma das decisões D1–D22 foi alterada materialmente pelo patch. D11 e D12 foram refinados por decisão anterior de D23 (patch anterior) e permanecem consistentes com esse refinamento. O patch QA-MODOS não alterou D11, D12 nem nenhuma outra decisão anterior.

---

## 16. Escopo Negativo

### 16.1 Busca focal por termos críticos

| Termo | Ocorrências na ADR auditada | Contexto | Avaliação |
|---|---|---|---|
| `conteúdo lógico completo` | §36.3 | Definição do escopo de medição QA-MODOS-001 | CORRETO |
| `maior largura` | §36.3 | Cálculo da coluna comum | CORRETO |
| `coluna comum` | §36.3 | Resultado da medição | CORRETO |
| `página` | §17.12, §18.8, §19, §20.5, §30, §31, §36.3, §46 | Regras de paginação e estabilidade entre páginas | CORRETO |
| `continuação` | §18.7, §19.8, §22, §26, §36.3 | Regras de continuação de linhas verbosas | CORRETO |
| `D23` | D23, §25, §39, §43, §44, §45, §46 | Política de modo; todas as referências coerentes | CORRETO |
| `nova tela` / `tela nova` / `telas novas ou revisadas` | D23 escopo, §25, §43, §44, §45, §46 | Distinção de escopo de D23 | CORRETO |
| `tela legada` / `telas legadas` | D23 escopo, §25, §39, §43, §44, §45, §46 | Compatibilidade preservada para legadas | CORRETO |
| `política ausente` | §43 item 3 (parentético) | Distinção: inválida para novas; compatibilidade para legadas | CORRETO |
| `default` | §43 item 3 (parentético) | "default implícito é proibido" para telas novas | CORRETO |
| `migração` | D23 escopo, §25, §39, §43 item 3 | Adiada para telas legadas | CORRETO |
| `H-0036` | D23 escopo, §39 | Exemplo histórico de tela legada; não exceção exclusiva | CORRETO |
| `matriz` | §3.3, §6, §39, §42, §46 verificação 2 | Exclusão explícita em todos os contextos | CORRETO — exclusão, não regra ativa |
| `matricial` | §6, §42 | Exclusão explícita | CORRETO — exclusão, não regra ativa |

### 16.2 Confirmação de exclusões preservadas

| Item excluído | Status |
|---|---|
| Conteúdo matricial (`tipo: matriz`) | EXCLUÍDO — §6, §42 |
| Distribuição matricial | EXCLUÍDO — §42 |
| Dashboard | EXCLUÍDO — §6, §42 |
| Lançador | EXCLUÍDO — §6, §42 |
| Outros componentes que não sejam `console` | EXCLUÍDO — §6, §42 |
| Integração concreta com Pipeline | EXCLUÍDO — §43 itens 10–15 |
| Persistência global | EXCLUÍDO — §24, §42 |
| Edição de JSON | EXCLUÍDO — §42 |
| Navegação interativa | EXCLUÍDO — §42 |
| Expansão ou recolhimento | EXCLUÍDO — §42 |
| Nova política global de fallback | EXCLUÍDO — §42 |

Nenhuma ocorrência de `matriz` ou `matricial` cria regra ativa. Todas as ocorrências são exclusões explícitas ou referências históricas.

---

## 17. Impacto sobre a Aplicação Documental

A aplicação documental anterior propagou D1–D22 antes da existência de D23. Com a aprovação da ADR-0028 revisada, uma nova etapa de aplicação documental será necessária para:

- propagar D23 (política de modo por tela: somente verbosa, somente não verbosa, alternável) aos contratos afetados;
- distinguir explicitamente telas novas ou revisadas de telas legadas nos contratos relevantes;
- propagar a regra de alinhamento de §36.3 ao contrato adequado;
- corrigir as divergências de `contrato_console.md §21.5 e §21.7`, `contrato_barra_de_menus.md §22.1` e `contrato_json_console.md §13.11` em relação a D23 (divergências classificadas como QA-MODOS-004, esperadas e preservadas como observação).

A nova aplicação não invalida a aplicação anterior de D1–D22 — complementa-a. Os critérios de §44 estão atualizados para orientar a nova etapa.

---

## 18. Impacto sobre H-0037

O handoff H-0037 permanece operacionalmente bloqueado (`BLOQUEADO_POR_MUDANCA_DOCUMENTAL`). A aprovação desta QA não libera implementação.

**Causa do bloqueio (inalterada):** os contratos ainda refletem o estado pré-D23. O H-0037, criado com base na aplicação D1–D22, especifica chip `[V] Verboso` em todas as telas de demonstração e cenários incompatíveis com as três políticas de D23.

**Sequência necessária para liberar H-0037:**

1. ADR-0028 aprovada neste ciclo de QA (esta etapa);
2. Nova aplicação documental incorporando D23 aos contratos;
3. Patch do H-0037 para: (a) separar cenários por política de modo; (b) remover chip das telas de modo único; (c) revisar fixtures; (d) estender schema para modo inicial não verboso;
4. Novo QA do H-0037 revisado.

---

## 19. Novos Achados

### 19.1 Pesquisa de novos achados

A busca focal, a auditoria de regressões e a verificação de todas as seções relevantes não identificaram defeito normativo, contradição material, decisão inventada ou regressão de escopo introduzida pelo patch.

Uma observação de baixa relevância foi examinada:

**Observação examinada — frontmatter `handoffs_bloqueados: []`**

O frontmatter da ADR-0028 mantém `handoffs_bloqueados: []`, enquanto o H-0037 está operacionalmente bloqueado. O bloqueio do H-0037 é estabelecido pelos relatórios de QA da sequência de ciclos e pela obrigação de re-aplicação documental antes da implementação. A omissão no frontmatter é de natureza administrativa, não normativa. A §47 última entrada e o §18 deste relatório registram o bloqueio e sua causa. Não constitui defeito corrigível neste ciclo.

**Decisão:** a observação não recebe ID formal. Não afeta a aprovação da ADR.

### 19.2 Resultado

```text
Novos achados bloqueantes: NENHUM
Novos achados altos: NENHUM
Novos achados médios: NENHUM
Novos achados baixos: NENHUM
Novas observações formais: NENHUMA
```

---

## 20. Conclusão

O patch corrigiu integralmente os dois achados corretivos identificados pelo QA de origem:

1. **QA-MODOS-001 (médio — corrigido):** §36.3 agora define explicitamente o escopo da medição de alinhamento como `conteúdo completo` (§27) restrito ao conteúdo lógico do cenário. A coluna é calculada sobre todos os textos identificadores do primeiro nível, é estável entre páginas, e as linhas de continuação permanecem alinhadas à mesma coluna inicial. A regra não cria largura fixa global nem se generaliza para outros cenários. O requisito de Determinismo (§13.6) é satisfeito.

2. **QA-MODOS-002 (baixo — corrigido):** D23 agora inclui subseção explícita sobre seu escopo de aplicação, distinguindo telas novas ou revisadas (política obrigatória, ausência inválida, default proibido) de telas legadas (compatibilidade preservada, reinterpretação proibida, migração adiada). §25, §39, §43 item 3, §44, §45 e §46 são coerentes com essa distinção. A tensão do QA de origem foi eliminada.

As observações não corretivas permanecem corretamente preservadas:

- **QA-MODOS-003:** cenário 3 inimplementável com schema atual; conceito decidido; schema adiado em §43 item 3. Observação preservada.
- **QA-MODOS-004:** contratos refletem estado pré-D23; reaplicação documental necessária. Observação preservada.

Nenhum novo achado formal foi identificado. Nenhuma decisão nova foi inventada. As três políticas estão normativamente distintas. Os quatro cenários mínimos estão íntegros. A regra de ausência de configuração diferencia corretamente telas novas de legadas. O escopo negativo permanece intacto. As decisões D1–D22 não foram afetadas.

A ADR-0028 revisada está pronta para nova aplicação documental incorporando D23.

---

## 21. Status Literal

```text
ADR_APPROVED_WITH_NOTES
```

---

## 22. Status Normalizado

```yaml
status_literal: ADR_APPROVED_WITH_NOTES
resultado_achados:
  QA-MODOS-001: CORRIGIDO
  QA-MODOS-002: CORRIGIDO
observacoes_de_origem:
  QA-MODOS-003: OBSERVACAO_PRESERVADA
  QA-MODOS-004: OBSERVACAO_PRESERVADA
novos_achados_bloqueantes: nenhum
novos_achados_altos: nenhum
novos_achados_medios: nenhum
novos_achados_baixos: nenhum
novas_observacoes: nenhuma
regressoes: nenhuma
bloqueio_decisao_usuario: false
bloqueio_arquitetural: false
```

---

## 23. Próxima Categoria

```yaml
proxima_categoria: APLICAR_ADR
escopo_da_nova_aplicacao:
  - "Propagar D23 (três políticas de modo) aos contratos afetados"
  - "Distinguir telas novas ou revisadas de telas legadas nos contratos"
  - "Propagar regra de alinhamento de §36.3 ao contrato adequado"
  - "Corrigir divergências de contrato_console.md, contrato_barra_de_menus.md e contrato_json_console.md identificadas em QA-MODOS-004"
restricoes:
  - "Nenhum ciclo de implementação (handoff) pode ser iniciado antes de APLICAR_ADR"
  - "A nova aplicação documental não deve alterar código"
  - "A nova aplicação documental não deve alterar a ADR-0028"
  - "O schema concreto dos campos de política e modo inicial permanece adiado; a aplicação pode propor nomes mas sem alterar comportamento já decidido"
  - "Após a nova aplicação, o H-0037 precisará ser patched antes de ser implementado"
```

(Fim do Relatório)
