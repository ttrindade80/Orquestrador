---
name: relatorio-qa-aplicacao-adr-0028-revisao-modos-por-tela
description: QA independente da aplicação documental da revisão D23 da ADR-0028 — política de modo por tela
metadata:
  type: relatorio_qa
  escopo: adr_application
  adr: ADR-0028
  revisao: D23
  data: 2026-07-18
  status_literal: ADR_APPLICATION_REJECTED
---

# Relatório de QA — Aplicação Documental da ADR-0028 (Revisão D23 — Política de Modo por Tela)

## 1. Cabeçalho e Identificação da Auditoria

| Campo | Valor |
|---|---|
| Tipo | QA_APLICACAO_ADR |
| ADR auditada | ADR-0028 |
| Revisão auditada | D23 — Política de modo por tela |
| Relatório de aplicação auditado | `RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` |
| Data de auditoria | 2026-07-18 |
| Status do relatório de aplicação declarado | `ADR_APPLICATION_COMPLETED` |
| Status desta auditoria | `ADR_APPLICATION_REJECTED` |
| Próxima categoria | `PATCH_APLICACAO_ADR` |

---

## 2. Declaração de Papel e Independência

Este relatório executa exclusivamente a função de **auditoria documental independente** da aplicação da revisão D23 da ADR-0028. O auditor:

- **não corrigiu** nenhum documento;
- **não alterou** o H-0037;
- **não implementou** nenhuma funcionalidade;
- **não preparou** stage nem commit;
- **não iniciou** outra etapa após a auditoria.

A auditoria foi conduzida como revisão de pares independente: o auditor leu os documentos de autoridade, comparou com os contratos modificados e o relatório de aplicação, e registra achados objetivos sem consideração do autor da aplicação.

---

## 3. Base Documental de Autoridade

A auditoria foi conduzida com base nas seguintes autoridades:

| Nível | Documento | Papel |
|---|---|---|
| Primário | ADR-0028 (D23, §25, §36.2, §36.3, §39, §44, §45, §46, §47) | Decisão arquitetural — fonte normativa da política de modo |
| Primário | `RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md` | QA anterior aprovado — estado pré-aplicação |
| Primário | `RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | Relatório da aplicação auditada |
| Secundário | `contrato_json_console.md` | Contrato da estrutura JSON do console |
| Secundário | `contrato_console.md` | Contrato do comportamento do console |
| Secundário | `contrato_tela_json.md` | Contrato do JSON estrutural da tela |
| Secundário | `contrato_barra_de_menus.md` | Contrato da barra de menus |
| Secundário | `contrato_composicao_corpo.md` | Contrato da composição do corpo |
| Secundário | `docs/NOMENCLATURA.md` | Glossário normativo |
| Secundário | `docs/adr/INDICE_ADR.md` | Índice de ADRs |

---

## 4. Autoridades Lidas e Confirmadas

| Documento | Extensão lida | Confirmação |
|---|---|---|
| ADR-0028 | Integral (1 477 linhas, incluindo §43, §44, §45, §46, §47) | CONFIRMADO |
| `RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md` | Integral | CONFIRMADO |
| `RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | Integral | CONFIRMADO |
| `contrato_json_console.md` | Integral (1 257 linhas, incluindo nova §13.13) | CONFIRMADO |
| `contrato_console.md` | Integral (840 linhas, incluindo nova §21.11) | CONFIRMADO |
| `contrato_tela_json.md` | Integral (1 470 linhas, incluindo nova §33.6) | CONFIRMADO |
| `contrato_barra_de_menus.md` | Integral (incluindo §14, §20, §22, §8.3) | CONFIRMADO |
| `contrato_composicao_corpo.md` | Integral (incluindo §4.4, §12.7, nova §12.8) | CONFIRMADO |
| `docs/NOMENCLATURA.md` | Seções §19.6 e §19.7 (nova) | CONFIRMADO |
| `docs/adr/INDICE_ADR.md` | Integral (63 linhas) | CONFIRMADO |

---

## 5. Estado Git Recebido

O auditor verificou o estado do repositório com `git status`, `git diff --stat` e `git diff --check`.

### 5.1 Estado antes de iniciar a auditoria (snapshot)

```
M  docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
(... outros arquivos não rastreados de sessões anteriores ...)
```

### 5.2 Arquivos modificados rastreados por git

```
git diff --stat
docs/NOMENCLATURA.md                        | 139 ++++++++++
docs/adr/INDICE_ADR.md                      |   1 +
docs/contratos/contrato_barra_de_menus.md   |  90 +++++++
docs/contratos/contrato_composicao_corpo.md |  92 +++++++
docs/contratos/contrato_console.md          | 165 ++++++++++++
docs/contratos/contrato_json_console.md     | 386 ++++++++++++++++++++++++++++
docs/contratos/contrato_tela_json.md        |  98 +++++++
7 files changed, 971 insertions(+)
```

### 5.3 Verificação de whitespace

```
git diff --check
(sem saída — nenhum problema de whitespace)
resultado: GIT_DIFF_CHECK_OK
```

### 5.4 Observação sobre a ADR-0028

A ADR-0028 aparece como `??` (arquivo não rastreado). Ela já era não rastreada antes desta aplicação — condição herdada das sessões anteriores, confirmada pelo QA de patch anterior. Portanto, as modificações ao §47 não são verificáveis via `git diff`. O conteúdo do §47 foi verificado por leitura direta e é consistente com o declarado na aplicação. Ver achado APLIC-MODOS-QA-005.

---

## 6. Inventário de Documentos Afetados — Declaração do Relatório de Aplicação

O relatório de aplicação declara os seguintes documentos como modificados ou criados:

| # | Caminho | Tipo declarado | Seções declaradas |
|---|---|---|---|
| 1 | `docs/contratos/contrato_json_console.md` | Modificação | §13.11, §13.12 (revisões) + §13.13 (nova) |
| 2 | `docs/contratos/contrato_console.md` | Modificação | §21.4, §21.5, §21.7, §21.10 (revisões) + §21.11 (nova) |
| 3 | `docs/contratos/contrato_tela_json.md` | Modificação | §33.2, §33.5 (revisões) + §33.6 (nova) |
| 4 | `docs/contratos/contrato_barra_de_menus.md` | Modificação | §22.1, §22.3, §22.7 (revisões) + §22.8 (nova) |
| 5 | `docs/contratos/contrato_composicao_corpo.md` | Modificação | §12.7 (revisão) + §12.8 (nova) |
| 6 | `docs/NOMENCLATURA.md` | Modificação | §19.6 (revisão) + §19.7 (nova) |
| 7 | `docs/adr/INDICE_ADR.md` | Modificação | Linha da ADR-0028 atualizada |
| 8 | `docs/adr/ADR-0028-...md` | Modificação | §47 — entrada de histórico adicionada |
| 9 | `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | Criação | Novo relatório |

---

## 7. Verificação de Inventário Real

### 7.1 Comparação declarado vs. real (git)

| Documento declarado | Status git | Verificável por diff | Avaliação |
|---|---|---|---|
| `contrato_json_console.md` | M (386 ins.) | Sim | CONFIRMADO |
| `contrato_console.md` | M (165 ins.) | Sim | CONFIRMADO |
| `contrato_tela_json.md` | M (98 ins.) | Sim | CONFIRMADO |
| `contrato_barra_de_menus.md` | M (90 ins.) | Sim | CONFIRMADO |
| `contrato_composicao_corpo.md` | M (92 ins.) | Sim | CONFIRMADO |
| `docs/NOMENCLATURA.md` | M (139 ins.) | Sim | CONFIRMADO |
| `docs/adr/INDICE_ADR.md` | M (1 ins.) | Sim | CONFIRMADO |
| `ADR-0028-....md` | ?? (untracked) | **Não** | Verificado por leitura direta — §47 presente e consistente |
| `RELATORIO_APLICACAO_...md` | ?? (novo/criado) | Indiretamente | CONFIRMADO |

### 7.2 Ausência de modificações não declaradas

O `git diff --stat` registra exatamente 7 arquivos rastreados modificados, todos declarados pela aplicação. Nenhum arquivo de código (`.py`), configuração (`config/`) ou handoff foi alterado. **CONFIRMADO**.

### 7.3 Ausência de deleções

O `git diff --stat` mostra `971 insertions(+)` e **0 deletions(-)**. Nenhum conteúdo existente foi removido. **CONFIRMADO**.

---

## 8. Decisões Auditadas (D23 e Escopo)

A aplicação declara propagar a revisão **D23** da ADR-0028, que formaliza:

- Três políticas de modo por tela: `somente_verboso`, `somente_nao_verboso`, `alternavel`
- Dois campos canônicos no JSON estrutural: `formato.excesso.politica_modo` e `formato.excesso.modo_inicial`
- Chip `[V] Verboso` e tecla `V` exclusivos de telas alternáveis
- Modo inicial obrigatório apenas para telas alternáveis
- Telas legadas (pré-D23) preservadas sem reinterpretação
- Quatro cenários futuros mínimos (§36.2)
- Regra de alinhamento de dois níveis (§36.3)
- Campo antigo `excesso.modo` supersedido para telas novas ou revisadas

Escopo da auditoria: confirmar que todos os contratos declarados refletem D23 de forma correta, completa e internamente consistente.

---

## 9. Campos Canônicos — Verificação

### 9.1 Localização declarada

Os campos são declarados no **JSON estrutural da tela** (elemento `console`), dentro de `formato.excesso`. **Não** estão no documento externo de conteúdo.

### 9.2 Verificação por contrato

| Contrato | Seção | Campo declarado corretamente | Avaliação |
|---|---|---|---|
| `contrato_json_console.md` | §13.13.1 | Sim — `formato.excesso.politica_modo` e `formato.excesso.modo_inicial` no JSON estrutural | CONFIRMADO |
| `contrato_console.md` | §21.7 | Sim — referência a `formato.excesso.politica_modo` | CONFIRMADO |
| `contrato_barra_de_menus.md` | §22.1, §22.3 | Sim — referência explícita a `formato.excesso.politica_modo` | CONFIRMADO |
| `contrato_tela_json.md` | §33.6.1 | Sim — localização no JSON estrutural | CONFIRMADO |
| `docs/NOMENCLATURA.md` | §19.7.2 | Sim — campos canônicos listados | CONFIRMADO |

### 9.3 Ausência dos campos no documento externo

O §13.13.6 declara: "A política não pode ser declarada no documento JSON externo de conteúdo — o documento externo não contém `politica_modo` nem `modo_inicial`." O §13.13.9 confirma a separação em tabela. **CONFIRMADO**.

---

## 10. Valores Canônicos — Verificação

### 10.1 Valores de `politica_modo`

Valores canônicos declarados em §13.13.2: `"somente_verboso"`, `"somente_nao_verboso"`, `"alternavel"`.

| Contrato | Seção | Valores listados | Avaliação |
|---|---|---|---|
| `contrato_json_console.md` | §13.13.2 | Três valores com comportamentos | CONFIRMADO |
| `contrato_barra_de_menus.md` | §22.8 | Tabela por política | CONFIRMADO |
| `docs/NOMENCLATURA.md` | §19.7.1 | Três políticas nomeadas | CONFIRMADO |

Valores simultâneos ativos: não existe nenhum quarto valor ativo concorrente. **CONFIRMADO**.

### 10.2 Valores de `modo_inicial`

Valores canônicos declarados em §13.13.2: `"verboso"` e `"nao_verboso"`.

| Contrato | Seção | Avaliação |
|---|---|---|
| `contrato_json_console.md` | §13.13.2 | Tabela com dois valores e comportamentos — CONFIRMADO |
| `contrato_console.md` | §21.7 | Referência a modo inicial por política — CONFIRMADO |

Aplicabilidade restrita a `alternavel`: confirmada em §13.13.2 ("aplicável apenas quando `politica_modo` for `"alternavel"`"). **CONFIRMADO**.

### 10.3 Ausência de valor desconhecido de `modo_inicial` na matriz

**ACHADO**: a matriz de §13.13.3 não inclui explicitamente a combinação `"alternavel" | valor_desconhecido | INVÁLIDO`. Ver seção 27, achado APLIC-MODOS-QA-001.

---

## 11. Matriz de Validade — Verificação

### 11.1 Conteúdo da matriz (§13.13.3)

| `politica_modo` | `modo_inicial` | Válido? |
|---|---|---|
| `"somente_verboso"` | ausente | **VÁLIDO** |
| `"somente_nao_verboso"` | ausente | **VÁLIDO** |
| `"alternavel"` | `"verboso"` | **VÁLIDO** |
| `"alternavel"` | `"nao_verboso"` | **VÁLIDO** |
| `"alternavel"` | ausente | **INVÁLIDO** |
| `"somente_verboso"` | qualquer valor | **INVÁLIDO** |
| `"somente_nao_verboso"` | qualquer valor | **INVÁLIDO** |
| valor desconhecido | qualquer | **INVÁLIDO** |
| ausente (tela nova ou revisada) | qualquer | **INVÁLIDO** |

A matriz cobre 4 combinações válidas e 5 inválidas, totalizando 9 entradas. A estrutura lógica está correta para os casos listados.

### 11.2 Casos exigidos pelo critério de auditoria

| Caso exigido | Presente na matriz ou proibições? | Avaliação |
|---|---|---|
| política desconhecida: inválido | Linha 8 — "valor desconhecido \| qualquer \| INVÁLIDO" | CONFIRMADO |
| **modo inicial desconhecido: inválido** | **Ausente** — §13.13.3 não inclui `"alternavel" \| valor_desconhecido \| INVÁLIDO` | **AUSENTE** |
| alternável sem modo inicial: inválido | Linha 5 — "alternavel \| ausente \| INVÁLIDO" | CONFIRMADO |
| política fixa com modo inicial: inválido | Linhas 6 e 7 | CONFIRMADO |
| alternável sem chip: incoerente | §33.6.4 de `contrato_tela_json.md` | CONFIRMADO |
| fixa com chip de alternância: incoerente | §33.6.4 de `contrato_tela_json.md` | CONFIRMADO |
| política no JSON externo: inválida | §13.13.6 e §13.13.9 | CONFIRMADO |
| política ausente em tela nova: inválida | Linha 9 e §13.13.6 | CONFIRMADO |
| tela legada sem política: preservada | §13.13.8 | CONFIRMADO |
| política inferida pelo chip: proibida | §22.1 de `contrato_barra_de_menus.md` | CONFIRMADO |
| política inferida por texto: proibida | §22.1 — "renderer não infere a política a partir do conteúdo externo nem de outra condição de ambiente" | CONFIRMADO |
| política inferida pelo campo antigo: proibida | §13.13.7 (dois mecanismos distintos, sem conflito) + §13.13.9 | CONFIRMADO |

**Lacuna confirmada**: `modo inicial desconhecido: inválido` não está presente na matriz nem nas proibições de §13.13.6. Ver achado APLIC-MODOS-QA-001.

---

## 12. Redundância e Determinismo — Verificação

| Caso | Avaliação |
|---|---|
| `somente_verboso` — modo único, sem `modo_inicial` necessário | CONFIRMADO — §13.13.3 linha 6 e §13.13.6 |
| `somente_nao_verboso` — modo único, sem `modo_inicial` necessário | CONFIRMADO |
| Política determina comportamento fixo sem ambiguidade | CONFIRMADO — §21.11.1 e §21.11.2 |
| `alternavel` usa `modo_inicial` para determinar abertura | CONFIRMADO — §13.13.3, §21.7 |
| Ausência de duplicação contraditória (política declarada em dois lugares) | CONFIRMADO — §13.13.6 e §13.13.9 proíbem declaração no externo |
| Default implícito proibido | CONFIRMADO — §13.13.6: "Não existe default implícito que substitua a declaração de `politica_modo`" |

---

## 13. Campo Legado `excesso.modo` — Verificação

| Critério | Seção | Avaliação |
|---|---|---|
| Campo descrito com semântica anterior ao D23 | §13.13.7 | CONFIRMADO |
| Campo supersedido para telas novas ou revisadas | §13.13.7 | CONFIRMADO |
| Campo não pode substituir `politica_modo` | §13.13.9 (separação estrutural/externo) | CONFIRMADO |
| Localização distinta: externo ≠ estrutural | §13.13.7 e §13.13.9 | CONFIRMADO |
| Tratamento histórico para telas legadas | §13.13.7 | CONFIRMADO |
| Arquivos reais não migrados | §11 do relatório de aplicação — "Nenhum arquivo de configuração JSON alterado" | CONFIRMADO |

O `excesso.modo` aparece no exemplo de §12.7 do documento externo de conteúdo — contexto correto. Não foi removido dos exemplos de telas legadas. **CONFIRMADO**.

---

## 14. Compatibilidade com Telas Legadas — Verificação

| Critério | Seção | Avaliação |
|---|---|---|
| Telas legadas permanecem válidas sem `politica_modo` | §13.13.8, §21.11.4, §33.6.3 | CONFIRMADO |
| Telas legadas não reinterpretadas automaticamente | §13.13.8: "não devem ser reinterpretadas automaticamente como uma das três políticas" | CONFIRMADO |
| Telas legadas não recebem política por inferência | §13.13.8: "não recebem política por inferência" | CONFIRMADO |
| Telas legadas não recebem `modo_inicial` por default | Não existe default implícito; legadas não declaram `modo_inicial` | CONFIRMADO |
| Nenhuma tela legada migrada nesta aplicação | Relatório §11 + `git diff --stat` (somente documentação) | CONFIRMADO |
| Migração futura adiada | §13.13.8 "até futura decisão de migração"; NOMENCLATURA §19.6 | CONFIRMADO |

### 14.1 Arquivos JSON identificados como telas legadas H-0036

A verificação direta confirmou que os seguintes 6 arquivos **não contêm** `politica_modo` nem `modo_inicial`:

- `config/telas/demo/h0036_conjuntos_conteudo.json`
- `config/telas/demo/h0036_console_conjuntos.json`
- `config/telas/demo/h0036_console_hierarquia.json`
- `config/telas/demo/h0036_console_tabela.json`
- `config/telas/demo/h0036_hierarquia_conteudo.json`
- `config/telas/demo/h0036_tabela_conteudo.json`

Esses arquivos estão na condição de compatibilidade legada declarada pelos contratos. O relatório de aplicação não os enumera nominalmente — ver achado APLIC-MODOS-QA-002 (item 5).

---

## 15. Distinção Autor/Carregador — Verificação

| Critério | Avaliação |
|---|---|
| Ausência de marcador `legacy: true` | Confirmado — nenhum dos contratos introduz esse marcador |
| Ausência de nova versão de schema | Confirmado — nenhum campo de versão de schema adicionado |
| Ausência de data de criação como marcador | Confirmado |
| Ausência de inferência automática por prefixo | Confirmado — §13.13.8 proíbe reinterpretação por inferência |
| Ausência de default global | Confirmado — §13.13.6 e §21.11 proíbem default implícito |
| Ausência de migração automática | Confirmado — §13.13.8 adia migração à decisão futura |

### 15.1 Limitação conhecida e devidamente registrada

A distinção loader entre "tela legada sem política" (válida) e "tela nova sem política" (inválida) não é implementável sem um marcador temporal ou flag. Essa limitação está corretamente registrada como decisão adiada no §43 item 3 da ADR e nos contratos (§13.13.8: "até futura decisão de migração"). Não é defeito introduzido por esta aplicação; é estado documentado e conscientemente adiado.

---

## 16. Barra de Menus — Verificação de Coerência

### 16.1 Seção nova §22 — Verificação

| Critério | Seção | Avaliação |
|---|---|---|
| Chip `[V]` obrigatório apenas em telas alternáveis | §22.1 | CONFIRMADO |
| Chip `[V]` condicionado a `politica_modo: "alternavel"` | §22.1 | CONFIRMADO |
| Chip derivado exclusivamente da política no JSON estrutural | §22.1 | CONFIRMADO |
| Renderer não infere política do conteúdo externo | §22.1 | CONFIRMADO |
| Modo inicial determinado pela política no JSON estrutural | §22.3 | CONFIRMADO |
| Tabela de presença/ausência do chip por política (3×2) | §22.8 | CONFIRMADO |
| Escopo restrito a conteúdo multinível | §22.5 | CONFIRMADO |

### 16.2 Inconsistências entre seções antigas e novas

| Seção antiga | Linguagem encontrada | Conflito com D23? | Avaliação |
|---|---|---|---|
| §14 "Modo verboso `[V]`" | "`[V]` só existe quando a instância de `console` declara que aceita modo verboso" | Pré-D23; sem referência a `politica_modo: "alternavel"` | OBSERVAÇÃO — mitigado por §22.5 (escopo) |
| §20 (Critérios de aceite) | "`[V]` só existe quando a instância de `console` declara que aceita modo verboso" | Critério não atualizado para D23 | BAIXO — ver achado APLIC-MODOS-QA-004 |
| §8.3 (tabela) | Entrada `[V]`: referência ao §14 | Cadeia de referência remete a linguagem pré-D23 | OBSERVAÇÃO |

A §22.5 declara explicitamente o escopo exclusivo, o que limita — mas não elimina — a ambiguidade da linguagem pré-D23 nas seções antigas.

---

## 17. JSON Estrutural — Verificação de Coerência

| Critério | Seção | Avaliação |
|---|---|---|
| Política e `modo_inicial` pertencem ao elemento `console` no JSON estrutural | §33.6.1 | CONFIRMADO |
| Conteúdo externo permanece separado | §33.1, §33.6.5 | CONFIRMADO |
| Barra coerente com política | §33.6.4 | CONFIRMADO |
| Alternável sem chip = incoerente | §33.6.4 | CONFIRMADO |
| Fixa com chip = incoerente | §33.6.4 | CONFIRMADO |
| Chip não pode inferir política | §33.6.4 e §22.1 | CONFIRMADO |
| Política não pode ser inferida do conteúdo | §33.6.5 | CONFIRMADO |

---

## 18. Composição do Corpo — Verificação

| Critério | Seção | Avaliação |
|---|---|---|
| Corpo não decide política de modo | §12.8 | CONFIRMADO |
| Corpo não infere política por linhas | §12.8 | CONFIRMADO |
| Corpo não infere política por distribuição | §12.8 | CONFIRMADO |
| Corpo preserva área alocada independentemente da política | §12.8 | CONFIRMADO |
| Corpo delega ao console | §12.8 | CONFIRMADO |

### 18.1 Linguagem pré-D23 em §4.4

O §4.4 de `contrato_composicao_corpo.md` ainda contém `tipo_exibicao: normal | verboso` como opção binária para o console, sem referência às três políticas D23. A §12.8 não substitui o §4.4 explicitamente. Esta é linguagem residual que cria aparência de política concorrente. Ver achado APLIC-MODOS-QA-004.

---

## 19. Nomenclatura — Verificação

| Critério | Seção | Avaliação |
|---|---|---|
| `política de modo` definida | §19.7.1 | CONFIRMADO |
| `somente verbosa` definida | §19.7.1 | CONFIRMADO |
| `somente não verbosa` definida | §19.7.1 | CONFIRMADO |
| `alternável` definida | §19.7.1 | CONFIRMADO |
| `modo inicial` definido | §19.7.1 | CONFIRMADO |
| `tela legada` definida | §19.7.1 | CONFIRMADO |
| Campos canônicos listados | §19.7.2 | CONFIRMADO |
| Distinções obrigatórias formuladas | §19.7.3 | CONFIRMADO |
| Uso ambíguo de `modo normal` | §19.7.4: "O termo `modo normal` não é sinônimo automático de `somente_nao_verboso`" | CONFIRMADO |
| Itens ainda deferidos atualizados | §19.6 | CONFIRMADO — migração de legadas permanece adiada; nomes dos campos removidos da lista de adiados |

---

## 20. Quatro Cenários Futuros Mínimos — Verificação

O §13.13.10 de `contrato_json_console.md` lista os quatro cenários futuros mínimos:

| Cenário | Presente | Avaliação |
|---|---|---|
| Tela somente não verbosa | Sim | CONFIRMADO |
| Tela somente verbosa | Sim | CONFIRMADO |
| Tela alternável de três níveis | Sim | CONFIRMADO |
| Tabela alternável | Sim | CONFIRMADO |

Nenhum arquivo real de configuração foi criado para esses cenários. Nenhuma profundidade máxima foi imposta. Nenhum conteúdo matricial foi associado. **CONFIRMADO**.

---

## 21. Alinhamento de Dois Níveis — Verificação

A regra de alinhamento em modo verboso (§36.3) foi propagada ao §13.13.11 de `contrato_json_console.md`.

| Critério | Avaliação |
|---|---|
| `elementos_medidos`: todos os identificadores do primeiro nível do conteúdo lógico completo do cenário | CONFIRMADO |
| `escopo`: conteúdo lógico do cenário (`conteudo_logico_completo_do_cenario`) | CONFIRMADO |
| `resultado`: coluna de início do segundo nível (`coluna_comum`) | CONFIRMADO |
| `recalculo_por_pagina`: coluna estável entre páginas — proibida | CONFIRMADO |
| `continuacao`: linhas de continuação do segundo nível alinham à mesma coluna inicial | CONFIRMADO |

---

## 22. Validações Normativas — Verificação

### 22.1 Validações de documentos afetados

| Validação | Origem | Avaliação |
|---|---|---|
| 1. Política desconhecida: inválido | §13.13.3 linha 8 | CONFIRMADO |
| 2. Modo inicial desconhecido: inválido | **Ausente** — §13.13.3 e §13.13.6 não tratam explicitamente | **AUSENTE** |
| 3. Alternável sem modo inicial: inválido | §13.13.3 linha 5 | CONFIRMADO |
| 4. Política fixa com modo inicial: inválido | §13.13.3 linhas 6–7 | CONFIRMADO |
| 5. Alternável sem chip: incoerente | §33.6.4 | CONFIRMADO |
| 6. Fixa com chip de alternância: incoerente | §33.6.4 | CONFIRMADO |
| 7. Política no JSON externo: inválida | §13.13.6 + §13.13.9 | CONFIRMADO |
| 8. Política ausente em tela nova: inválida | §13.13.3 linha 9 + §13.13.6 | CONFIRMADO |
| 9. Tela legada sem política: preservada | §13.13.8 | CONFIRMADO |
| 10. Política inferida pelo chip: proibida | §22.1 | CONFIRMADO |
| 11. Política inferida por texto: proibida | §22.1 | CONFIRMADO |
| 12. Política inferida pelo campo antigo: proibida | §13.13.7 + §13.13.9 | CONFIRMADO |

**11 de 12 validações confirmadas. 1 ausente (validação 2).**

---

## 23. Índice ADR e Histórico — Verificação

### 23.1 Índice ADR

| Critério | Avaliação |
|---|---|
| Entrada ADR-0028 atualizada com D23 | CONFIRMADO |
| Três políticas mencionadas por nome | CONFIRMADO |
| Campos canônicos (`formato.excesso.politica_modo`, `formato.excesso.modo_inicial`) | CONFIRMADO |
| Chip `[V]` e tecla `V` restritos a telas alternáveis | CONFIRMADO |
| Telas legadas preservadas | CONFIRMADO |
| Quatro cenários futuros | CONFIRMADO |
| Alinhamento de dois níveis | CONFIRMADO |
| Aplicação documental D1–D22 (2026-07-17) e D23 (2026-07-18) registradas | CONFIRMADO |
| Status: "aceita e aplicada" | CONFIRMADO |

### 23.2 Histórico da ADR (§47)

| Critério | Avaliação |
|---|---|
| Entrada de 2026-07-18 presente | CONFIRMADO — verificado por leitura direta |
| Campos canônicos declarados | CONFIRMADO — `formato.excesso.politica_modo` e `formato.excesso.modo_inicial` |
| Todos os contratos modificados listados | CONFIRMADO |
| Não afirma que QA foi aprovado | CONFIRMADO |
| Não altera decisões aprovadas (D1–D22, D23, §25, §36, §39, §43, §44, §45, §46) | CONFIRMADO — apenas §47 foi adicionado |

### 23.3 Inconsistência §43 item 3

O §43 item 3 ainda contém a frase "mecanismo concreto de schema adiado" apesar de o §47 registrar que os campos canônicos foram definidos. Esta inconsistência interna não é contradição normativa material — os contratos são a autoridade para a definição dos campos — mas cria ambiguidade textual na ADR. Ver achado APLIC-MODOS-QA-003.

---

## 24. Relatório de Aplicação — Verificação Estrutural

### 24.1 Seções presentes

| Seção exigida | Presente? | Avaliação |
|---|---|---|
| Autoridades (decisões aplicadas) | Sim — Seção 2 | CONFIRMADO |
| Alcance da nova aplicação | Sim — Seções 2.1–2.6 | CONFIRMADO |
| Representação concreta dos campos | Sim — Seção 13 | CONFIRMADO |
| Matriz de validade resumida | Sim — Seção 14 | CONFIRMADO |
| Inventário do campo antigo (`excesso.modo`) | Sim — Seção 13 | CONFIRMADO |
| Alterações por arquivo | Sim — Seções 3–10 | CONFIRMADO |
| Quatro cenários futuros | Sim — Seção 2.4 | CONFIRMADO |
| Alinhamento de dois níveis | Sim — Seção 2.5 | CONFIRMADO |
| Arquivos preservados | Sim — Seção 11 | CONFIRMADO |
| Ausência de implementação | Sim — Seção 11 | CONFIRMADO |
| Conclusão sem autoaprovação | Sim — Seção 17 declara `ADR_APPLICATION_COMPLETED`, não QA | CONFIRMADO |
| Aplicação anterior preservada | Sim — Seção 11 | CONFIRMADO |

### 24.2 Seções ausentes

| Seção exigida | Presente? | Avaliação |
|---|---|---|
| **Estado Git inicial** | **Não** | **AUSENTE** |
| **Diff real** (saída de `git diff`) | **Não** | **AUSENTE** |
| **Resultado de `git diff --check`** | **Não** | **AUSENTE** |
| **Seção de resíduos** (busca de linguagem pré-D23 residual) | **Não** | **AUSENTE** |
| **Inventário nominal de telas legadas** (arquivos JSON individuais) | **Não** (menciona H-0036 genericamente) | **AUSENTE** |

Cinco seções estruturalmente exigidas estão ausentes do relatório de aplicação. Ver achado APLIC-MODOS-QA-002.

---

## 25. Escopo e Ausência de Implementação — Verificação

| Critério | Fonte de verificação | Avaliação |
|---|---|---|
| H-0037 não alterado | Relatório §11 + git status (H-0037 não aparece em M) | CONFIRMADO |
| `config/` não alterado | `git diff --stat` — sem arquivos de config | CONFIRMADO |
| `demo/` não alterado | `git diff --stat` + `git status` | CONFIRMADO |
| `tela/` não alterado | `git diff --stat` + `git status` | CONFIRMADO |
| Nenhum fixture novo criado | Verificado por `find config/ -name "*.json"` — todos pré-existentes | CONFIRMADO |
| Nenhum código alterado | `git diff --stat` — apenas arquivos `.md` | CONFIRMADO |
| Nenhum teste criado | Verificado | CONFIRMADO |
| Apenas arquivos de documentação modificados | `git diff --stat` — 7 arquivos `.md` | CONFIRMADO |

---

## 26. Busca de Resíduos — Verificação

O auditor realizou varredura de termos potencialmente residuais nos documentos modificados.

### 26.1 Termos verificados

| Termo | Contexto encontrado | Avaliação |
|---|---|---|
| `excesso.modo` | §13.13.7 (documentação de campo legado) e §21 (referência histórica) | CORRETO — contexto documental |
| `modo normal` | §19.7.4 (NOMENCLATURA — desambiguação explícita) | CORRETO |
| `[V]` nas novas seções | §22 (barra) e §21.11 (console) — condicionado a `alternavel` | CORRETO |
| `modo verboso` nas novas seções | Associado a política — CORRETO | CORRETO |
| `politica_modo` | Presente em todos os contratos nas seções novas — CORRETO | CORRETO |
| `modo_inicial` | Presente nas seções novas com obrigatoriedade condicionada — CORRETO | CORRETO |

### 26.2 Resíduos identificados (linguagem pré-D23 em seções antigas não atualizadas)

| Arquivo | Seção | Termo residual | Impacto |
|---|---|---|---|
| `contrato_barra_de_menus.md` | §14 | "`[V]` só existe quando a instância de `console` declara que aceita modo verboso" | Pré-D23, sem referência a `politica_modo: "alternavel"` |
| `contrato_barra_de_menus.md` | §20 | Critério: "`[V]` só existe quando a instância de `console` declara que aceita modo verboso" | Critério não atualizado |
| `contrato_composicao_corpo.md` | §4.4 | `tipo_exibicao: normal \| verboso` | Opção binária pré-D23 |
| `contrato_tela_json.md` | §14 | "o chip/tecla `[V]` alterna modo verboso quando a instância permite" | Sem escopo D23 |
| `contrato_console.md` | §6 | "modo normal é o default" | Sem escopo multinível; §21.11 proíbe default para multinível |

Resíduos mitigados pelas declarações de escopo nas novas seções (§21.1, §22.5). Não constituem contradição normativa material, mas criam ambiguidade para leitores que não leiam as seções novas. Ver achado APLIC-MODOS-QA-004.

---

## 27. Achados da Auditoria

### APLIC-MODOS-QA-001 — MÉDIO — Corretivo

**Título**: Modo inicial desconhecido não explicitado como INVÁLIDO na matriz de validade

**Arquivo**: `docs/contratos/contrato_json_console.md`

**Seções afetadas**: §13.13.3 (Matriz de validade) e §13.13.6 (Proibições)

**Descrição**: A auditoria confirma que a validação normativa exige cobertura explícita do caso `"alternavel" | valor_desconhecido_para_modo_inicial | INVÁLIDO`. A matriz de §13.13.3 não inclui essa combinação. O §13.13.2 define apenas dois valores admitidos para `modo_inicial` (`"verboso"` e `"nao_verboso"`), e o §13.13.6 não declara explicitamente que qualquer outro valor é inválido.

Comparação: a matriz inclui `valor desconhecido` para `politica_modo` → INVÁLIDO (linha 8), mas não o caso análogo para `modo_inicial`.

**Impacto**: Um implementador pode não rejeitar explicitamente um `modo_inicial` com valor fora dos dois canônicos (ex.: `"verbose"`, `"0"`, `"true"`). A norma exige presença explícita desta proibição.

**Correção proposta**: Adicionar ao §13.13.3:
```
| `"alternavel"` | valor desconhecido | **INVÁLIDO** — valor de `modo_inicial` não pertence ao conjunto admitido |
```
Ou acrescentar ao §13.13.6: "Valor desconhecido de `modo_inicial` é inválido; os únicos valores admitidos são `"verboso"` e `"nao_verboso"`."

---

### APLIC-MODOS-QA-002 — MÉDIO — Corretivo

**Título**: Relatório de aplicação estruturalmente incompleto

**Arquivo**: `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`

**Seção afetada**: Estrutura do relatório

**Descrição**: O relatório de aplicação está ausente das seguintes seções estruturalmente exigidas:

1. **Estado Git inicial** — nenhuma seção apresenta o estado do repositório no início da operação;
2. **Diff real** — nenhuma saída de `git diff` é incluída; o relatório descreve em prosa o que mudou, mas não apresenta os diffs concretos para verificação independente. O diff real obtido pelo auditor: `7 files changed, 971 insertions(+)`;
3. **Resultado de `git diff --check`** — ausente. Resultado verificado pelo auditor: `GIT_DIFF_CHECK_OK`;
4. **Seção de resíduos** — não há seção dedicada à busca e identificação de linguagem pré-D23 residual nos documentos modificados;
5. **Inventário nominal de telas legadas** — o relatório menciona H-0036 apenas como "exemplo histórico de tela legada". Os 6 arquivos JSON nominalmente afetados pela política de compatibilidade legada não são listados.

**Impacto**: Auditores subsequentes não podem verificar a integridade da aplicação de forma completa apenas pelo relatório. O diff real é necessário para confirmar que apenas as modificações declaradas foram realizadas. O inventário nominal delimita o escopo concreto da compatibilidade preservada.

**Correção proposta**: Complementar o relatório com: (a) seção de estado git ao início com `git status` e `git diff --stat`; (b) seção com saída completa de `git diff`; (c) resultado de `git diff --check`; (d) seção de busca de resíduos com resultado da varredura; (e) lista nominal dos 6 arquivos JSON de telas legadas H-0036.

---

### APLIC-MODOS-QA-003 — BAIXO — Observação

**Título**: Inconsistência interna da ADR — §43 item 3 vs. §47

**Arquivo**: `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`

**Seções afetadas**: §43 item 3 e §47

**Descrição**: O §43 item 3 ainda contém a frase "mecanismo concreto de schema adiado" enquanto o §47 (entrada 2026-07-18) registra que os campos canônicos foram definidos pela aplicação. A inconsistência é interna à ADR: §43 diz "adiado", §47 diz "definido".

Esta inconsistência não é contradição normativa material — os contratos são a autoridade para os nomes dos campos, e a aplicação documental propagou os nomes corretamente a todos os contratos. O §43 não foi modificado porque a regra de aplicação proíbe alterar o corpo de decisões aprovadas. Contudo, leitores do §43 sem ler o §47 encontrarão informação desatualizada.

Adicionalmente, a ADR aparece como `??` (não rastreada) no git, limitando a auditabilidade via `git diff`.

**Impacto**: Ambiguidade para leitores futuros do §43. Não bloqueia a aplicação.

**Recomendação**: Registrar como item de patch futuro — atualizar o texto do §43 item 3 para refletir que os nomes concretos foram definidos pela aplicação documental de 2026-07-18.

---

### APLIC-MODOS-QA-004 — BAIXO — Observação

**Título**: Seções pré-D23 não reconciliadas em múltiplos contratos

**Arquivos**: `contrato_barra_de_menus.md`, `contrato_composicao_corpo.md`, `contrato_tela_json.md`, `contrato_console.md`

**Seções afetadas**: §14 (barra), §20 (barra), §4.4 (corpo), §14 (tela_json), §6 (console)

**Descrição**: Seções anteriores a D23, não incluídas no escopo declarado da aplicação, contêm linguagem que não referencia a nova terminologia D23:

- `contrato_barra_de_menus.md` §14 e §20: usam "quando a instância de `console` declara que aceita modo verboso" sem referência a `politica_modo: "alternavel"`;
- `contrato_composicao_corpo.md` §4.4: mantém `tipo_exibicao: normal | verboso` como opção binária;
- `contrato_tela_json.md` §14: usa "quando a instância permite" sem escopo D23;
- `contrato_console.md` §6: "modo normal é o default" sem escopo D23.

As novas seções (§21.1, §22.5) declaram explicitamente que D23 se aplica exclusivamente a conteúdo multinível, o que mitiga — mas não elimina — a ambiguidade.

**Impacto**: Dupla linguagem pode confundir implementadores que leiam seções antigas sem as novas. Mitigado pelas declarações de escopo.

**Recomendação**: Reconciliar as seções antigas em futura revisão dos contratos afetados.

---

### APLIC-MODOS-QA-005 — OBSERVAÇÃO

**Título**: ADR-0028 não rastreada por git — rastreabilidade limitada

**Arquivo**: `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`

**Descrição**: O arquivo da ADR aparece como `??` (não rastreado) no `git status`. Esta condição é herdada de sessões anteriores — o arquivo nunca foi committed ao repositório. O `git diff` não registra a adição do §47 declarada pela aplicação. A modificação foi verificada por leitura direta: o §47 contém a entrada de 2026-07-18 com os campos canônicos definidos, consistente com o declarado. Não é um defeito introduzido por esta aplicação.

**Impacto**: Auditores não podem verificar a modificação via `git diff`. A rastreabilidade da ADR depende de leitura direta.

---

### APLIC-MODOS-QA-006 — OBSERVAÇÃO

**Título**: Inventário nominal de telas legadas ausente do relatório de aplicação

**Arquivo**: `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`

**Descrição**: O relatório menciona H-0036 como "exemplo histórico" mas não nomeia os 6 arquivos JSON de `config/telas/demo/h0036_*.json`. A verificação direta pelo auditor confirmou que nenhum desses arquivos contém `politica_modo` ou `modo_inicial`. Este achado está incorporado ao APLIC-MODOS-QA-002 como item 5.

---

## 28. Tabela de Achados

| ID | Arquivo principal | Seção | Severidade | Tipo | Status |
|---|---|---|---|---|---|
| APLIC-MODOS-QA-001 | `contrato_json_console.md` | §13.13.3 | MÉDIO | Corretivo | Requer correção |
| APLIC-MODOS-QA-002 | `RELATORIO_APLICACAO_...md` | Estrutura | MÉDIO | Corretivo | Requer correção |
| APLIC-MODOS-QA-003 | `ADR-0028.md` | §43 item 3 | BAIXO | Observação | Registrado |
| APLIC-MODOS-QA-004 | Múltiplos contratos | Seções pré-D23 | BAIXO | Observação | Registrado |
| APLIC-MODOS-QA-005 | `ADR-0028.md` | Rastreabilidade git | OBSERVAÇÃO | Informativo | Registrado |
| APLIC-MODOS-QA-006 | `RELATORIO_APLICACAO_...md` | Inventário | OBSERVAÇÃO | Incorporado ao QA-002 | Registrado |

---

## 29. Relação com Achados de QAs Anteriores

| Achado anterior | Status reportado | Verificação nesta auditoria |
|---|---|---|
| QA-MODOS-001 (contrato_json_console §13.11) | Corrigido | CONFIRMADO — §13.11 corretamente distingue telas alternáveis e de modo único |
| QA-MODOS-002 (contrato_console §21.5) | Corrigido | CONFIRMADO — §21.5 condiciona V a `politica_modo: "alternavel"` |
| QA-MODOS-003 (contrato_barra §22 estrutura) | Observação preservada | CONFIRMADO — §22 presente e correto |
| QA-MODOS-004 (ADR §46 verificações) | Observação preservada | CONFIRMADO — §46 intacto |

Nenhum achado anterior foi reaberto por esta aplicação. Os quatro achados foram tratados conforme declarado.

---

## 30. Análise de Severidade e Impacto

### 30.1 Achados MÉDIOS (corretivos)

**APLIC-MODOS-QA-001** — A lacuna na matriz de validade é um defeito normativo concreto: a regra de rejeição de `modo_inicial` com valor fora do conjunto admitido não está explicitamente declarada. Implementadores conscientes podem inferi-la do §13.13.2, mas a norma exige explicitação. O risco é baixo na prática (poucos erros de digitação produziriam um valor inexistente), mas o defeito documental é real e corrigível.

**APLIC-MODOS-QA-002** — A ausência do diff real, do resultado de `git diff --check`, da seção de resíduos e do inventário nominal de legadas não compromete a validade das modificações realizadas — que foram verificadas pelo auditor e estão corretas. O defeito é processual: o relatório de aplicação é um artefato de auditoria e sua incompletude reduz a rastreabilidade para sessões futuras.

### 30.2 Achados BAIXOS e observações

APLIC-MODOS-QA-003, QA-004, QA-005 e QA-006 não afetam a corretude das modificações realizadas. São registrados para subsidiar futuras revisões dos contratos e do processo.

### 30.3 Avaliação do conteúdo das modificações

O conteúdo das 8 modificações documentais é substancialmente correto. A revisão D23 foi propagada de forma consistente a todos os contratos declarados. A lógica das três políticas, dos campos canônicos, da matriz de validade (exceto o caso omitido de APLIC-MODOS-QA-001), da compatibilidade legada e dos cenários futuros está corretamente expressa.

---

## 31. Correções Necessárias

Para que a aplicação seja aprovada (`ADR_APPLICATION_APPROVED` ou `ADR_APPLICATION_APPROVED_WITH_NOTES`), as seguintes correções são necessárias:

### Correção C-001 (para APLIC-MODOS-QA-001)

Arquivo: `docs/contratos/contrato_json_console.md`

Adicionar ao §13.13.3 a linha:
```
| `"alternavel"` | valor desconhecido | **INVÁLIDO** — valor de `modo_inicial` não pertence ao conjunto admitido (`"verboso"` ou `"nao_verboso"`) |
```

Ou, alternativamente, acrescentar ao §13.13.6 a proibição explícita:
> "Valor de `modo_inicial` fora do conjunto admitido (`"verboso"`, `"nao_verboso"`) é inválido."

### Correção C-002 (para APLIC-MODOS-QA-002)

Arquivo: `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`

Adicionar ao relatório:
- Seção de estado Git inicial (ou complementar seção existente)
- Seção com diff real completo (`git diff` dos 7 arquivos rastreados)
- Resultado de `git diff --check` (verificado: `GIT_DIFF_CHECK_OK`)
- Seção de busca de resíduos documentais
- Lista nominal das 6 telas legadas H-0036 afetadas pela compatibilidade D23

---

## 32. Conclusão e Status

### 32.1 Avaliação global

A aplicação documental da revisão D23 da ADR-0028 propagou corretamente as três políticas de modo (`somente_verboso`, `somente_nao_verboso`, `alternavel`), os dois campos canônicos (`formato.excesso.politica_modo` e `formato.excesso.modo_inicial`), a compatibilidade com telas legadas, os quatro cenários futuros e a regra de alinhamento de dois níveis a todos os 7 contratos rastreados.

Dois defeitos de severidade MÉDIO foram identificados:

1. A matriz de validade de `contrato_json_console.md` §13.13.3 não cobre explicitamente o caso `"alternavel" | valor_desconhecido_para_modo_inicial | INVÁLIDO`;
2. O relatório de aplicação está estruturalmente incompleto (ausência de diff real, `git diff --check`, estado git inicial, seção de resíduos e inventário nominal de telas legadas).

Ambos os defeitos são corrigíveis sem nova decisão arquitetural.

### 32.2 Decisão de bloqueio do H-0037

O H-0037 permanece na condição `BLOQUEADO_POR_MUDANCA_DOCUMENTAL`. A afirmação do relatório de aplicação de que o bloqueio pode ser levantado **não é confirmada por esta auditoria**. O bloqueio somente pode ser levantado após aprovação desta auditoria (`ADR_APPLICATION_APPROVED` ou `ADR_APPLICATION_APPROVED_WITH_NOTES`).

### 32.3 Status literal

```
status_literal: ADR_APPLICATION_REJECTED
proxima_categoria: PATCH_APLICACAO_ADR
```

---

## 33. Bloco de Saída Final

```yaml
qa_type: QA_APLICACAO_ADR
adr: ADR-0028
revisao_auditada: D23
data_auditoria: 2026-07-18

status_literal: ADR_APPLICATION_REJECTED
proxima_categoria: PATCH_APLICACAO_ADR

relatorio_aplicacao_auditado: docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
relatorio_qa_gerado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md

achados:
  - id: APLIC-MODOS-QA-001
    severidade: MEDIO
    tipo: corretivo
    arquivo: docs/contratos/contrato_json_console.md
    secao: "§13.13.3"
    titulo: "Modo inicial desconhecido não explicitado como INVÁLIDO na matriz de validade"
    correcao: "Adicionar linha à matriz ou proibição explícita ao §13.13.6"

  - id: APLIC-MODOS-QA-002
    severidade: MEDIO
    tipo: corretivo
    arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
    secao: "estrutura do relatório"
    titulo: "Relatório de aplicação estruturalmente incompleto"
    correcao: "Adicionar: estado git inicial, diff real, resultado de git diff --check, seção de resíduos, inventário nominal de telas legadas H-0036"

  - id: APLIC-MODOS-QA-003
    severidade: BAIXO
    tipo: observacao
    arquivo: docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
    secao: "§43 item 3"
    titulo: "Inconsistência interna da ADR — §43 diz 'adiado', §47 diz 'definido'"
    correcao: "Patch futuro ao §43 item 3"

  - id: APLIC-MODOS-QA-004
    severidade: BAIXO
    tipo: observacao
    arquivos:
      - docs/contratos/contrato_barra_de_menus.md
      - docs/contratos/contrato_composicao_corpo.md
      - docs/contratos/contrato_tela_json.md
      - docs/contratos/contrato_console.md
    titulo: "Seções pré-D23 não reconciliadas em múltiplos contratos"
    correcao: "Reconciliar em futuras revisões dos contratos"

  - id: APLIC-MODOS-QA-005
    severidade: OBSERVACAO
    tipo: informativo
    arquivo: docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
    titulo: "ADR não rastreada por git — rastreabilidade limitada"

  - id: APLIC-MODOS-QA-006
    severidade: OBSERVACAO
    tipo: incorporado_ao_QA-002
    titulo: "Inventário nominal de telas legadas ausente do relatório de aplicação"

achados_anteriores_confirmados:
  - QA-MODOS-001: corrigido — CONFIRMADO
  - QA-MODOS-002: corrigido — CONFIRMADO
  - QA-MODOS-003: observacao — CONFIRMADO
  - QA-MODOS-004: observacao — CONFIRMADO

git_diff_check: GIT_DIFF_CHECK_OK
arquivos_modificados_rastreados: 7
insercoes_totais: 971
delecoes_totais: 0

telas_legadas_h0036_verificadas:
  - config/telas/demo/h0036_conjuntos_conteudo.json
  - config/telas/demo/h0036_console_conjuntos.json
  - config/telas/demo/h0036_console_hierarquia.json
  - config/telas/demo/h0036_console_tabela.json
  - config/telas/demo/h0036_hierarquia_conteudo.json
  - config/telas/demo/h0036_tabela_conteudo.json
campo_politica_modo_ausente_em_todas: true

h0037_status: BLOQUEADO_POR_MUDANCA_DOCUMENTAL
h0037_desbloqueio_autorizado: false

conteudo_modificacoes_substancialmente_correto: true
defeitos_bloqueantes: false
defeitos_corrigiveis: 2
observacoes: 4
```
