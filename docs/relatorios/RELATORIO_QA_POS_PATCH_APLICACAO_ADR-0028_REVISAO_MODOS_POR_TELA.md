---
name: relatorio-qa-pos-patch-aplicacao-adr-0028-revisao-modos-por-tela
description: QA pós-patch da aplicação documental da revisão D23 da ADR-0028 — verifica correção de APLIC-MODOS-QA-001 e APLIC-MODOS-QA-002, preservação de APLIC-MODOS-QA-003, APLIC-MODOS-QA-004 e APLIC-MODOS-QA-005, ausência de regressões e fidelidade do relatório de aplicação patched.
metadata:
  type: relatorio_qa_pos_patch_aplicacao_adr
  escopo: adr_application_patch
  adr: ADR-0028
  revisao: D23
  data: 2026-07-18
  status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
---

# Relatório de QA Pós-Patch — Aplicação Documental da ADR-0028 (Revisão D23 — Política de Modo por Tela)

---

## 1. Identificação

| Campo | Valor |
|---|---|
| Tipo | QA_POS_PATCH_APLICACAO_ADR |
| ADR auditada | ADR-0028 |
| Revisão auditada | D23 — Política de modo por tela |
| QA de origem | `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` |
| Status de origem | `ADR_APPLICATION_REJECTED` |
| Relatório de aplicação auditado | `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` |
| Data de auditoria | 2026-07-18 |
| Status desta auditoria | `ADR_APPLICATION_APPROVED_WITH_NOTES` |
| Próxima categoria | `PATCH_HANDOFF` |
| Handoff | H-0037 |

---

## 2. Declaração de Papel e Independência

Este relatório executa exclusivamente a função de **auditoria documental independente pós-patch** da aplicação da revisão D23 da ADR-0028. O auditor:

- **não corrigiu** nenhum documento;
- **não alterou** a ADR;
- **não alterou** contratos;
- **não alterou** o H-0037;
- **não implementou** nenhuma funcionalidade;
- **não preparou** stage nem commit;
- **não iniciou** outra etapa após a auditoria.

---

## 3. Base Documental

| Nível | Documento | Papel |
|---|---|---|
| Primário | ADR-0028 (D23, §25, §36.2, §36.3, §43, §47) | Decisão arquitetural — fonte normativa |
| Primário | `RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | QA de origem — achados a verificar |
| Primário | `RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | Relatório patched — objeto principal desta auditoria |
| Secundário | `contrato_json_console.md` | Contrato patched — verificação de APLIC-MODOS-QA-001 |
| Secundário | `contrato_console.md`, `contrato_tela_json.md`, `contrato_barra_de_menus.md`, `contrato_composicao_corpo.md` | Verificação de preservação (APLIC-MODOS-QA-004) |
| Secundário | `RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md` | QA precedente — contexto de aplicação |
| Referência | `demo/demo.py`, `config/telas/demo/` | Verificação do inventário legado H-0036 |

---

## 4. Estado Git Atual

Executados na raiz do repositório:

```
git status --short

 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
?? docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_ADR-0028.md
?? docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md
?? tela/__pycache__/
```

```
git diff --check
(sem saída)
GIT_DIFF_CHECK_OK
```

```
git diff --name-status

M	docs/NOMENCLATURA.md
M	docs/adr/INDICE_ADR.md
M	docs/contratos/contrato_barra_de_menus.md
M	docs/contratos/contrato_composicao_corpo.md
M	docs/contratos/contrato_console.md
M	docs/contratos/contrato_json_console.md
M	docs/contratos/contrato_tela_json.md
```

```
git diff --stat

 docs/NOMENCLATURA.md                        | 139 ++++++++++
 docs/adr/INDICE_ADR.md                      |   1 +
 docs/contratos/contrato_barra_de_menus.md   |  90 +++++++
 docs/contratos/contrato_composicao_corpo.md |  92 +++++++
 docs/contratos/contrato_console.md          | 165 ++++++++++++
 docs/contratos/contrato_json_console.md     | 388 ++++++++++++++++++++++++++++
 7 files changed, 973 insertions(+)
```

```
git diff --cached --name-only
(vazio — stage vazio)
```

### 4.1 Observações sobre o estado Git

**Arquivos rastreados modificados (M):** 7 — mesmos da aplicação original.

**ADR-0028:** `??` (não rastreada) — condição herdada de sessões anteriores, não criada pelo patch.

**H-0037:** `??` (não rastreado) — não modificado pelo patch. Confirmado.

**RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md:** `??` (não rastreado) — modificado pelo patch com adição das seções 18–22; não aparece em `git diff`.

**Stage:** vazio. Confirmado.

**Arquivo inesperado:** `?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md` — arquivo não rastreado preexistente de etapa anterior (sem `_REVISAO_MODOS_POR_TELA`). Não pertence a este patch.

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

Não interfere na presente auditoria.

### 4.2 Comparação com estado declarado no patch

| Item declarado | Estado atual | Avaliação |
|---|---|---|
| branch: master | Confirmado | ✓ |
| HEAD: f6982d0 | Confirmado (`git log` — HEAD é f6982d0) | ✓ |
| stage: vazio | Confirmado | ✓ |
| GIT_DIFF_CHECK_OK | Confirmado | ✓ |
| arquivos_rastreados_modificados: 7 | Confirmado | ✓ |
| novos_arquivos_criados_pelo_patch: 0 | Confirmado — nenhum novo arquivo rastreado | ✓ |
| H_0037_alterado: false | Confirmado — `??` não rastreado, sem M | ✓ |
| implementacao_realizada: false | Confirmado — `git diff --stat` mostra apenas `.md` | ✓ |

---

## 5. QA de Origem

| Campo | Valor |
|---|---|
| Arquivo | `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` |
| Status | `ADR_APPLICATION_REJECTED` |
| Achados corretivos | APLIC-MODOS-QA-001 (MÉDIO), APLIC-MODOS-QA-002 (MÉDIO) |
| Observações não corretivas | APLIC-MODOS-QA-003 (BAIXO), APLIC-MODOS-QA-004 (BAIXO), APLIC-MODOS-QA-005 (OBSERVAÇÃO) |

---

## 6. Patch Recebido

| Item | Valor declarado | Confirmado |
|---|---|---|
| Arquivo modificado 1 | `docs/contratos/contrato_json_console.md` | Sim — M no git status |
| Arquivo modificado 2 | `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | Sim — `??` (untracked, criado na aplic. original) |
| Outros arquivos alterados | nenhum | Confirmado |
| H-0037 alterado | false | Confirmado |
| Implementação realizada | false | Confirmado |
| Status pós-patch | `APLICACAO_ADR_PATCHED` | Informado |

### 6.1 Alterações confirmadas por `git diff`

O `git diff --stat` mostra `contrato_json_console.md` com **388 inserções** (+2 em relação ao QA de origem, que registrava 386). A diferença de 2 inserções corresponde às duas linhas adicionadas pelo patch:

1. Linha na matriz §13.13.3: `| "alternavel" | valor desconhecido | INVÁLIDO |`
2. Frase em §13.13.6 definindo "valor desconhecido" de `modo_inicial`

Confirmado por `git diff -- docs/contratos/contrato_json_console.md`:
```diff
+| `"alternavel"` | valor desconhecido | **INVÁLIDO** — valor de `modo_inicial` não pertence ao conjunto admitido (`"verboso"` ou `"nao_verboso"`) |
+- Valor desconhecido de `modo_inicial` é inválido; os únicos valores admitidos são `"verboso"` e `"nao_verboso"`. "Valor desconhecido" designa qualquer valor que não pertença a esse conjunto.
```

---

## 7. Verificação de APLIC-MODOS-QA-001

### 7.1 Achado original

A matriz de validade de `contrato_json_console.md §13.13.3` não declarava explicitamente que uma tela com `politica_modo: "alternavel"` e `modo_inicial` com valor desconhecido é inválida.

### 7.2 Matriz auditada (§13.13.3 atual)

| `politica_modo` | `modo_inicial` | Válido? |
|---|---|---|
| `"somente_verboso"` | ausente | **VÁLIDO** |
| `"somente_nao_verboso"` | ausente | **VÁLIDO** |
| `"alternavel"` | `"verboso"` | **VÁLIDO** |
| `"alternavel"` | `"nao_verboso"` | **VÁLIDO** |
| `"alternavel"` | ausente | **INVÁLIDO** — modo inicial obrigatório |
| `"alternavel"` | valor desconhecido | **INVÁLIDO** — valor de `modo_inicial` não pertence ao conjunto admitido (`"verboso"` ou `"nao_verboso"`) |
| `"somente_verboso"` | qualquer valor | **INVÁLIDO** — modo inicial proibido em política fixa |
| `"somente_nao_verboso"` | qualquer valor | **INVÁLIDO** — modo inicial proibido em política fixa |
| valor desconhecido | qualquer | **INVÁLIDO** |
| ausente (tela nova ou revisada) | qualquer | **INVÁLIDO** — ausência de política é inválida |

**10 entradas** (9 da aplicação original + 1 adicionada pelo patch).

### 7.3 Verificação da linha nova

| Critério | Avaliação |
|---|---|
| Linha presente na matriz normativa (não apenas em explicação) | CONFIRMADO — linha na tabela de §13.13.3 |
| Únicos valores válidos continuam sendo `"verboso"` e `"nao_verboso"` | CONFIRMADO — §13.13.2 e nova frase em §13.13.6 |
| `modo_inicial` continua permitido somente em `"alternavel"` | CONFIRMADO — §13.13.2, §13.13.3 e §13.13.6 |
| Telas fixas continuam proibidas de declarar `modo_inicial` | CONFIRMADO — linhas 7 e 8 da matriz |
| Não foi criado default implícito | CONFIRMADO — §13.13.6: "Não existe default implícito..." |
| Não foi criado valor alternativo | CONFIRMADO — conjunto admitido não expandido |
| Tratamento de telas legadas não alterado | CONFIRMADO — §13.13.8 intacto |
| Exemplos válidos e inválidos anteriores preservados | CONFIRMADO — §13.13.4 e §13.13.5 intactos |
| Sem contradição com outros contratos | CONFIRMADO — apenas contrato_json_console.md modificado |

### 7.4 Verificação da cláusula em §13.13.6

A frase adicionada ao §13.13.6:

> "Valor desconhecido de `modo_inicial` é inválido; os únicos valores admitidos são `"verboso"` e `"nao_verboso"`. "Valor desconhecido" designa qualquer valor que não pertença a esse conjunto."

Define explicitamente o conceito de "valor desconhecido" como qualquer valor fora de `{"verboso", "nao_verboso"}`. Confirmado por leitura direta do arquivo.

### 7.5 Matriz completa exigida pelo critério de auditoria

| Caso exigido | Presente | Avaliação |
|---|---|---|
| `somente_verboso` \| ausente \| válido | Linha 1 | CONFIRMADO |
| `somente_nao_verboso` \| ausente \| válido | Linha 2 | CONFIRMADO |
| `alternavel` \| `verboso` \| válido | Linha 3 | CONFIRMADO |
| `alternavel` \| `nao_verboso` \| válido | Linha 4 | CONFIRMADO |
| `somente_verboso` \| qualquer valor presente \| inválido | Linha 7 | CONFIRMADO |
| `somente_nao_verboso` \| qualquer valor presente \| inválido | Linha 8 | CONFIRMADO |
| `alternavel` \| ausente \| inválido | Linha 5 | CONFIRMADO |
| `alternavel` \| valor desconhecido \| inválido | **Linha 6 — NOVA** | CONFIRMADO |
| política desconhecida \| qualquer \| inválido | Linha 9 | CONFIRMADO |

**Todos os 9 casos exigidos presentes.**

### 7.6 Classificação

```
CORRIGIDO
```

---

## 8. Verificação de APLIC-MODOS-QA-002

### 8.1 Achado original

O relatório de aplicação estava estruturalmente incompleto: faltavam estado Git inicial, diff real, resultado de `git diff --check`, seção de resíduos e inventário nominal dos seis itens legados H-0036.

### 8.2 Seções exigidas — presença no relatório patched

| Seção exigida | Presente | Avaliação |
|---|---|---|
| Estado Git inicial (§18) | Sim — seção 18 (§18.1, §18.2, §18.3) | CONFIRMADO |
| Diff real (§19) | Sim — seção 19 com quatro subsecções | CONFIRMADO |
| Busca de resíduos (§20) | Sim — seção 20 com tabela e confirmações | CONFIRMADO |
| Inventário nominal H-0036 (§21) | Sim — seção 21 com 6 itens individuais | CONFIRMADO |
| Correção pós-QA (§22) | Sim — seção 22 com referências explícitas | CONFIRMADO |

---

## 9. Estado Git Inicial registrado no relatório

### 9.1 Classificação das informações

O relatório §18.1 distingue três categorias:

- **Observação direta**: dados coletados durante a etapa de patch (PATCH_APLICACAO_ADR, 2026-07-18) — claramente identificados como tal.
- **Reconstrução evidenciada**: dados inferíveis com evidência de relatórios preservados e histórico Git.
- **Não recuperável**: formulado como `NAO_RECONSTRUIVEL_COM_EVIDENCIA_DISPONIVEL`.

A distinção está presente e explícita. Nenhuma reconstrução é apresentada como observação direta. ✓

### 9.2 Campos obrigatórios

| Campo | Presente | Valor declarado | Avaliação |
|---|---|---|---|
| `branch` | Sim — §18.3 | `master` (reconstrução — comprovável por git log) | CONFIRMADO |
| `head` | Sim — §18.3 | `f6982d0` (reconstrução — comprovável) | CONFIRMADO |
| `stage` | Sim — §18.3 | `NAO_RECONSTRUIVEL_COM_EVIDENCIA_DISPONIVEL` | CONFIRMADO — uso correto |
| `arquivos_modificados_acumulados` | Sim — §18.3 | `NAO_RECONSTRUIVEL_COM_EVIDENCIA_DISPONIVEL` | CONFIRMADO — uso correto |
| `arquivos_nao_rastreados_acumulados` | Sim — §18.3 | ADR como pré-existente; relatório como criado durante etapa; outros NR | CONFIRMADO |
| `arquivos_inesperados` | Sim — §18.3 | `nenhum identificado` | CONFIRMADO |

---

## 10. Inventário da Aplicação

### 10.1 Classificação declarada

| Classificação | Quantidade | Arquivos |
|---|---|---|
| Semânticamente modificados pela aplicação | 8 | 7 rastreados + ADR não rastreada |
| Criados pela aplicação | 1 | `RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` |
| **Total** | **9** | |

O relatório declara em §16 os 8 modificados (incluindo ADR não rastreada) e o relatório criado. A §19.5 e §19.6 distinguem explicitamente os arquivos não rastreados da verificação por `git diff`. O relatório distingue corretamente:

| Distinção | Presente | Avaliação |
|---|---|---|
| Arquivo semanticamente modificado pela aplicação | Sim — §16 (8 entradas) | CONFIRMADO |
| Arquivo rastreado pelo Git | Sim — §19.1 (7 arquivos M) | CONFIRMADO |
| Arquivo não rastreado (ADR) | Sim — §19.5: verificado por leitura direta | CONFIRMADO |
| Relatório criado (não rastreado) | Sim — §19.6 | CONFIRMADO |

O fato de o Git mostrar 7 arquivos rastreados modificados não reduz a contagem semântica de 8 modificados. A ADR permanece não rastreada e sua modificação é verificada por leitura direta. ✓

---

## 11. Diff Real

### 11.1 Comandos registrados

| Comando | Registrado em | Avaliação |
|---|---|---|
| `git diff --name-status` | §19.1 | CONFIRMADO |
| `git diff --stat` | §19.2 | CONFIRMADO |
| `git diff --check` | §19.3 | CONFIRMADO |
| `git diff --cached --name-only` | §19.4 | CONFIRMADO |

### 11.2 Estatística declarada no relatório vs. estado atual

| Item | Relatório (§19.2) | Estado atual | Diferença |
|---|---|---|---|
| `contrato_json_console.md` | 386 ins. | 388 ins. | +2 (linhas do patch) |
| Total inserções | 971 | 973 | +2 |
| Total arquivos | 7 | 7 | 0 |
| Deletions | 0 | 0 | 0 |

A diferença de +2 inserções é exatamente o que o patch acrescentou a `contrato_json_console.md` (1 linha na matriz + 1 frase nas proibições). O diff no relatório foi coletado antes da modificação do contrato (estado pré-fix), enquanto o estado atual reflete o estado pós-fix. Ambos são consistentes. A divergência está explicitamente endereçada pelo critério de auditoria.

### 11.3 Verificações complementares

| Critério | Avaliação |
|---|---|
| `git diff --check` = GIT_DIFF_CHECK_OK | CONFIRMADO — §19.3 e confirmado pelo auditor |
| Stage vazio | CONFIRMADO — §19.4 e confirmado pelo auditor |
| Diferença tracked/untracked explicada | CONFIRMADO — §19.5 (ADR) e §19.6 (relatório) |
| Nenhum diff alegado para arquivo não rastreado sem leitura direta | CONFIRMADO — ADR verificada por leitura direta (§19.5) |
| Arquivo técnico inesperado | Nenhum detectado pelo auditor |

---

## 12. Busca de Resíduos

O relatório §20 apresenta seção dedicada com:

- §20.1: tabela de termos pesquisados nas **adições** dos arquivos modificados (termos: `excesso.modo`, `politica_modo`, `modo_inicial`, `normal`, `verboso`, `nao_verboso`, `[V] Verboso`, `toda tela`, `tela legada`, `default`, `migração`, `matriz`, `matricial`, `mesmos dados`, `dois modos`);
- §20.2: resíduos em seções antigas (pré-D23, fora do escopo da aplicação);
- §20.3: confirmações normativas.

### 12.1 Verificação das confirmações normativas (§20.3)

| Confirmação | Declarada | Avaliação |
|---|---|---|
| Nenhuma regra ativa exige alternância em toda tela | Sim — §21.1 e §22.5 | CONFIRMADO |
| Nenhuma regra ativa exige chip em tela fixa | Sim — §22.1 e §22.8 | CONFIRMADO |
| Telas novas não recebem default | Sim — §13.13.6 proíbe default implícito | CONFIRMADO |
| Telas legadas não são reinterpretadas | Sim — §13.13.8 | CONFIRMADO |
| `excesso.modo` antigo não é forma canônica de D23 | Sim — §13.13.7 | CONFIRMADO |
| Conteúdo matricial excluído | Sim — §13.13.11 e ADR-0025 mencionadas | CONFIRMADO |
| Política não aparece no documento externo | Sim — §13.13.6 e §13.13.9 | CONFIRMADO |

---

## 13. Inventário Nominal do Legado H-0036

### 13.1 Composição no repositório real

```bash
ls config/telas/demo/h0036_*
```

Arquivos confirmados pelo auditor:
```
config/telas/demo/h0036_conjuntos_conteudo.json
config/telas/demo/h0036_console_conjuntos.json
config/telas/demo/h0036_console_hierarquia.json
config/telas/demo/h0036_console_tabela.json
config/telas/demo/h0036_hierarquia_conteudo.json
config/telas/demo/h0036_tabela_conteudo.json
```

Total: 6 itens. Composição: 3 telas estruturais + 3 documentos externos de conteúdo. ✓

### 13.2 Verificação dos campos D23

```bash
grep -l "politica_modo\|modo_inicial" config/telas/demo/*.json
```

Resultado: nenhum arquivo `h0036_*.json` contém `politica_modo` ou `modo_inicial`. Confirmado. ✓

(Observação: `demo.json` e `h0036_console_unico.json` — que não são arquivos H-0036 — contêm esses termos. São arquivos pré-existentes de ciclos anteriores, não modificados pelo patch.)

### 13.3 Associações declaradas no relatório vs. demo.py

Associações em `demo.py` (linhas 136–138):
```python
"h0036_console_hierarquia": "h0036_hierarquia_conteudo",
"h0036_console_tabela": "h0036_tabela_conteudo",
"h0036_console_conjuntos": "h0036_conjuntos_conteudo",
```

Associações declaradas no relatório §21:

| Item do relatório | Tipo | Caminho | Associação | Avaliação |
|---|---|---|---|---|
| h0036_console_hierarquia | tela_estrutural | `config/telas/demo/h0036_console_hierarquia.json` | h0036_hierarquia_conteudo | CONFIRMADO |
| h0036_console_tabela | tela_estrutural | `config/telas/demo/h0036_console_tabela.json` | h0036_tabela_conteudo | CONFIRMADO |
| h0036_console_conjuntos | tela_estrutural | `config/telas/demo/h0036_console_conjuntos.json` | h0036_conjuntos_conteudo | CONFIRMADO |
| h0036_hierarquia_conteudo | conteudo_externo | `config/telas/demo/h0036_hierarquia_conteudo.json` | h0036_console_hierarquia | CONFIRMADO |
| h0036_tabela_conteudo | conteudo_externo | `config/telas/demo/h0036_tabela_conteudo.json` | h0036_console_tabela | CONFIRMADO |
| h0036_conjuntos_conteudo | conteudo_externo | `config/telas/demo/h0036_conjuntos_conteudo.json` | h0036_console_conjuntos | CONFIRMADO |

O relatório **não** denomina os 6 itens indiscriminadamente como "seis telas" — distingue explicitamente "três telas estruturais" e "três documentos externos de conteúdo". ✓

Ausência dos campos D23 em todos os 6 arquivos: CONFIRMADA. ✓
Tratamento como legado preservado: CONFIRMADO — `legado_preservado`, `reinterpretacao_automatica: proibida`, `migracao_nesta_etapa: nao`. ✓

---

## 14. Correção Pós-QA (§22 do relatório patched)

### 14.1 Estrutura declarada

| Campo | Declarado | Confirmado |
|---|---|---|
| `qa_de_origem` | `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | CONFIRMADO |
| `status_de_origem` | `ADR_APPLICATION_REJECTED` | CONFIRMADO |
| APLIC-MODOS-QA-001 tratado | Sim — §22.2 | CONFIRMADO |
| APLIC-MODOS-QA-002 tratado | Sim — §22.2 | CONFIRMADO |
| APLIC-MODOS-QA-003 preservado | Sim — §22.3 | CONFIRMADO |
| APLIC-MODOS-QA-004 preservado | Sim — §22.3 | CONFIRMADO |
| APLIC-MODOS-QA-005 preservado | Sim — §22.3 | CONFIRMADO |

### 14.2 Status pós-patch declarado pelo relatório

```yaml
status_pos_patch: AGUARDA_QA_POS_PATCH
proxima_categoria: QA_POS_PATCH_APLICACAO_ADR
```

O relatório **não declara a aplicação formalmente aprovada**. Declara apenas que os achados corretivos foram tratados e aguarda QA pós-patch. ✓

---

## 15. Tratamento de APLIC-MODOS-QA-003

**Achado original**: inconsistência entre §43 item 3 (diz "mecanismo concreto de schema adiado") e §47 (registra que os campos canônicos foram definidos pela aplicação de 2026-07-18).

### 15.1 Verificação

| Critério | Evidência | Avaliação |
|---|---|---|
| ADR não alterada pelo patch | ADR ainda `??` no git status; git diff não registra modificação | CONFIRMADO |
| §43 item 3 intacto | Leitura direta: "mecanismo concreto de schema adiado" permanece na segunda frase do item 3 | CONFIRMADO |
| §47 intacto | Leitura direta: entrada de 2026-07-18 presente e inalterada | CONFIRMADO |
| Observação registrada como não corretiva em §22.3 | Sim — "ADR preservada; §43 não pode ser alterado sem nova decisão" | CONFIRMADO |
| Relatório não a declara corrigida | CONFIRMADO — §22.3 categoriza como `observacoes_nao_tratadas_como_patch` | CONFIRMADO |
| Nenhuma mudança de schema adicional introduzida | Confirmado — apenas contrato_json_console.md modificado | CONFIRMADO |

### 15.2 Classificação

```
OBSERVACAO_PRESERVADA
```

---

## 16. Tratamento de APLIC-MODOS-QA-004

**Achado original**: seções pré-D23 não reconciliadas em `contrato_barra_de_menus.md` §14/§20, `contrato_composicao_corpo.md` §4.4, `contrato_tela_json.md` §14, `contrato_console.md` §6.

### 16.1 Verificação

| Critério | Avaliação |
|---|---|
| `contrato_barra_de_menus.md` não alterado pelo patch | CONFIRMADO — modificado apenas pela aplicação original, não pelo patch |
| `contrato_composicao_corpo.md` não alterado pelo patch | CONFIRMADO |
| `contrato_tela_json.md` não alterado pelo patch | CONFIRMADO |
| `contrato_console.md` não alterado pelo patch | CONFIRMADO |
| Observação não transformada em patch amplo | CONFIRMADO — §22.3: "Outros contratos fora do escopo deste patch; aguarda futura revisão editorial" |
| Nenhuma nova divergência material introduzida | CONFIRMADO — nenhum contrato adicional modificado |
| Conteúdo normativo substancial aprovado permanece coerente | CONFIRMADO — seções novas D23 com escopo explícito (§21.1, §22.5) mitigam ambiguidade |

### 16.2 Classificação

```
OBSERVACAO_PRESERVADA
```

---

## 17. Tratamento de APLIC-MODOS-QA-005

**Achado original**: ADR-0028 não rastreada por git — rastreabilidade limitada.

### 17.1 Verificação

| Critério | Evidência | Avaliação |
|---|---|---|
| ADR continua não rastreada | `?? docs/adr/ADR-0028-...` em `git status --short` | CONFIRMADO |
| Patch não adicionou ADR ao stage | `git diff --cached --name-only` vazio | CONFIRMADO |
| Nenhum commit executado | `git log` — HEAD permanece f6982d0 | CONFIRMADO |
| Observação permanece não corretiva | §22.3: "Estado de rastreamento não alterado; ADR preservada" | CONFIRMADO |

### 17.2 Classificação

```
OBSERVACAO_PRESERVADA
```

---

## 18. Ausência de Regressão Normativa

### 18.1 Campos canônicos preservados

| Campo | Caminho | Valores | Avaliação |
|---|---|---|---|
| `politica_modo` | `formato.excesso.politica_modo` | `somente_verboso`, `somente_nao_verboso`, `alternavel` | CONFIRMADO — §13.13.2 intacto |
| `modo_inicial` | `formato.excesso.modo_inicial` | `verboso`, `nao_verboso` | CONFIRMADO — §13.13.2 intacto |

### 18.2 Regras normativas preservadas

| Regra | Avaliação |
|---|---|
| Política obrigatória em telas novas ou revisadas | CONFIRMADO — §13.13.3 linha 10 e §13.13.6 |
| Política ausente inválida em telas novas | CONFIRMADO |
| Ausência de default implícito | CONFIRMADO — §13.13.6 |
| Compatibilidade nominal de telas legadas | CONFIRMADO — §13.13.8 intacto |
| Campo `excesso.modo` antigo não canônico para D23 | CONFIRMADO — §13.13.7 intacto |
| Quatro cenários futuros mínimos | CONFIRMADO — §13.13.10 intacto |
| Alinhamento determinístico de dois níveis | CONFIRMADO — §13.13.11 intacto |
| Ausência de conteúdo matricial | CONFIRMADO — §42 da ADR; escopo negativo preservado |
| Ausência de implementação | CONFIRMADO — `git diff --stat` mostra apenas `.md` |
| Bloqueio operacional do H-0037 | CONFIRMADO — H-0037 não modificado; sem commit; bloqueio só levantado após aprovação desta auditoria |

---

## 19. Escopo do Patch

### 19.1 Arquivos modificados pelo patch

| Arquivo | Tipo | Modificação | Confirmado |
|---|---|---|---|
| `docs/contratos/contrato_json_console.md` | Rastreado (M) | +2 inserções: linha em §13.13.3 e frase em §13.13.6 | Sim — `git diff --stat` |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | Não rastreado (`??`) | Seções 18–22 adicionadas | Sim — leitura direta |

### 19.2 Arquivos não modificados pelo patch

Os 6 outros arquivos rastreados modificados (`NOMENCLATURA.md`, `INDICE_ADR.md`, `contrato_barra_de_menus.md`, `contrato_composicao_corpo.md`, `contrato_console.md`, `contrato_tela_json.md`) são resultado da aplicação original, não do patch. O patch não acrescentou alterações a eles. ✓

### 19.3 Verificação de alterações não declaradas

O `git diff --stat` confirma exatamente 7 arquivos rastreados modificados, todos da aplicação original. O patch não alterou nenhum arquivo além dos dois declarados. ✓

---

## 20. Novos Achados

### APLIC-MODOS-QAPP-001 — BAIXO

**Título**: Matriz de validade resumida na seção 14 do relatório de aplicação não inclui o caso corrigido

**Arquivo**: `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`

**Seção**: §14 — Matriz de validade (resumo normativo)

**Evidência**: A seção 14 do relatório (sumário da aplicação, criado na etapa original) apresenta 8 entradas, sem incluir `"alternavel" | valor desconhecido | INVÁLIDO`. O patch adicionou essa entrada ao contrato (`§13.13.3`) e documentou a correção em `§22.2`, mas não atualizou a tabela resumo de §14. A tabela de §14 é, portanto, inconsistente com a matriz normativa atual.

**Autoridade**: A matriz normativa é a de `contrato_json_console.md §13.13.3` (corrigida pelo patch). O §14 do relatório é um sumário histórico da aplicação original.

**Severidade**: baixo

**Impacto**: Um leitor que consulte apenas o relatório de aplicação (sem ler o contrato) verá a matriz incompleta. O contrato é a autoridade; o sumário é auxiliar. Não bloqueia a aprovação.

**Correção necessária**: Não para aprovação desta auditoria. Recomendado em futura revisão editorial do relatório.

**Necessidade de decisão do usuário**: Não.

---

### APLIC-MODOS-QAPP-002 — OBSERVAÇÃO

**Título**: Estatística de diff no relatório (971 inserções) não reflete o estado final após o patch (973 inserções)

**Arquivo**: `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`

**Seção**: §19.2

**Evidência**: O relatório registra `7 files changed, 971 insertions(+)` em §19.2. O estado atual é `973 insertions`. A diferença de +2 corresponde exatamente às duas linhas adicionadas pelo patch a `contrato_json_console.md`. A coleta ocorreu antes da modificação do contrato.

**Autoridade**: Critério de auditoria explícito: "Não rejeite apenas porque a quantidade de inserções mudou de 971 para 973, desde que isso corresponda ao patch real." A diferença corresponde ao patch real.

**Severidade**: observação

**Impacto**: Nenhum normativo. Informação de contexto.

---

## 21. Conclusão

### 21.1 Achados corretivos

Ambos os achados corretivos (`APLIC-MODOS-QA-001` e `APLIC-MODOS-QA-002`) foram endereçados pelo patch:

- **APLIC-MODOS-QA-001**: linha adicionada à matriz normativa e cláusula definitória adicionada às proibições. A cobertura do caso `"alternavel" | valor desconhecido | INVÁLIDO` está agora explícita e na seção normativa correta.
- **APLIC-MODOS-QA-002**: cinco seções adicionadas ao relatório (§18–§22), cobrindo estado Git inicial com classificação tripartida, diff real com os quatro comandos, busca de resíduos e inventário nominal dos 6 itens H-0036.

### 21.2 Observações não corretivas

As três observações de origem (`APLIC-MODOS-QA-003`, `APLIC-MODOS-QA-004`, `APLIC-MODOS-QA-005`) foram preservadas sem tratamento como patch, conforme correspondente à sua natureza não corretiva.

### 21.3 Novos achados

Dois novos achados identificados: `APLIC-MODOS-QAPP-001` (baixo) e `APLIC-MODOS-QAPP-002` (observação). Nenhum é bloqueante.

### 21.4 Avaliação global

O conteúdo normativo da aplicação — três políticas de modo, dois campos canônicos, matriz de validade (agora com 10 entradas), compatibilidade de telas legadas, quatro cenários futuros e regra de alinhamento — está correto e completo em todos os contratos. O relatório de aplicação está estruturalmente completo após o patch. Nenhuma regressão foi identificada.

---

## 22. Status Literal

```
ADR_APPLICATION_APPROVED_WITH_NOTES
```

Achados corretivos tratados. Observações remanescentes são não corretivas: APLIC-MODOS-QA-003 (inconsistência interna da ADR), APLIC-MODOS-QA-004 (seções pré-D23 em contratos), APLIC-MODOS-QA-005 (ADR não rastreada), APLIC-MODOS-QAPP-001 (sumário de matriz incompleto no relatório), APLIC-MODOS-QAPP-002 (estatística de diff pré-fix).

---

## 23. Status Normalizado

```yaml
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
aprovado: true
com_notas: true
bloqueante_pendente: false
```

---

## 24. Próxima Categoria

```yaml
proxima_categoria: PATCH_HANDOFF
handoff: H-0037
```

O H-0037 pode agora ser desbloqueado da condição `BLOQUEADO_POR_MUDANCA_DOCUMENTAL` e prosseguir para a etapa `PATCH_HANDOFF`.

---

## 25. Bloco de Saída Final

```yaml
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
status_normalizado:
  aprovado: true
  com_notas: true
  bloqueante_pendente: false

relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
qa_de_origem: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
relatorio_de_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md

resultado_achados:
  APLIC-MODOS-QA-001: CORRIGIDO
  APLIC-MODOS-QA-002: CORRIGIDO

observacoes_de_origem:
  APLIC-MODOS-QA-003: OBSERVACAO_PRESERVADA
  APLIC-MODOS-QA-004: OBSERVACAO_PRESERVADA
  APLIC-MODOS-QA-005: OBSERVACAO_PRESERVADA

novos_achados_bloqueantes: nenhum
novos_achados_altos: nenhum
novos_achados_medios: nenhum
novos_achados_baixos:
  - id: APLIC-MODOS-QAPP-001
    titulo: "Sumário de matriz em §14 do relatório de aplicação não inclui o caso corrigido"
    arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
    secao: §14
    bloqueante: false
novas_observacoes:
  - id: APLIC-MODOS-QAPP-002
    titulo: "Estatística de diff em §19.2 (971) não reflete estado final do patch (973)"
    arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
    secao: §19.2
    bloqueante: false

regressoes: nenhuma

matriz:
  alternavel_com_modo_desconhecido: INVALIDO — presente na linha 6 de §13.13.3
  valores_validos: verboso, nao_verboso

relatorio_de_aplicacao:
  estado_git_inicial:
    secao: §18
    classificacao_presente: true
    campos_obrigatorios_presentes: true
    distincao_observacao_vs_reconstrucao: CONFIRMADA
  inventario:
    modificados: 8
    criados: 1
    total: 9
  diff_real:
    secao: §19
    comandos_registrados: 4
    stat_declarado: "7 files changed, 971 insertions(+)"
    stat_atual: "7 files changed, 973 insertions(+)"
    diferenca_justificada: "+2 linhas do patch — aceito pelo critério de auditoria"
  git_diff_check: GIT_DIFF_CHECK_OK
  residuos:
    secao: §20
    termos_cobertos: 15
    confirmacoes_normativas: 7

inventario_legado_H_0036:
  total: 6
  telas_estruturais:
    - h0036_console_hierarquia (config/telas/demo/h0036_console_hierarquia.json)
    - h0036_console_tabela (config/telas/demo/h0036_console_tabela.json)
    - h0036_console_conjuntos (config/telas/demo/h0036_console_conjuntos.json)
  documentos_externos:
    - h0036_hierarquia_conteudo (config/telas/demo/h0036_hierarquia_conteudo.json)
    - h0036_tabela_conteudo (config/telas/demo/h0036_tabela_conteudo.json)
    - h0036_conjuntos_conteudo (config/telas/demo/h0036_conjuntos_conteudo.json)
  associacoes:
    h0036_console_hierarquia: h0036_hierarquia_conteudo
    h0036_console_tabela: h0036_tabela_conteudo
    h0036_console_conjuntos: h0036_conjuntos_conteudo
  campos_D23_ausentes_em_todos: true
  indiscriminadamente_chamados_de_telas: false

observacoes_preservadas:
  APLIC-MODOS-QA-003: true
  APLIC-MODOS-QA-004: true
  APLIC-MODOS-QA-005: true

escopo_do_patch:
  arquivos_confirmados:
    - docs/contratos/contrato_json_console.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
  outros_arquivos_alterados: false

H_0037_alterado: false
implementacao_realizada: false

git:
  branch: master
  head: f6982d0
  stage: vazio
  git_diff_check: GIT_DIFF_CHECK_OK
  arquivos_rastreados_modificados: 7
  insercoes_atuais: 973
  delecoes: 0
  adr_rastreada: false

proxima_categoria: PATCH_HANDOFF
handoff: H-0037
```
