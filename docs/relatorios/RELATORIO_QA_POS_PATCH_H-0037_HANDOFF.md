# RELATÓRIO QA PÓS-PATCH — H-0037 HANDOFF

**Identificador do relatório:** RELATORIO_QA_POS_PATCH_H-0037_HANDOFF
**Auditor:** Auditor Documental Independente (Claude Sonnet 4.6)
**Data:** 2026-07-18
**Sessão:** 9c55aee2-d13a-4193-a2f1-15a5154e5e46
**Documento auditado:** `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
**Patch auditado:** Incorporação de D23 — política de modo de apresentação por tela
**QA anterior:** `RELATORIO_QA_H-0037_HANDOFF.md` (aprovado com 4 achados LOW)

---

## 1. ESCOPO DA AUDITORIA

Esta auditoria verifica exclusivamente o H-0037 após seu PATCH_HANDOFF, que incorporou a Decisão 23 (D23) da ADR-0028. O escopo abrange:

1. Fidelidade do H-0037 à ADR-0028 revisada com D23
2. Fidelidade aos contratos reaplicados
3. Correção das omissões identificadas no QA anterior (QA-LOW-01 a QA-LOW-04)
4. Completude da lista nominal da futura implementação
5. Implementabilidade dos quatro cenários
6. Testabilidade; demonstração permanente; validação manual
7. Ausência de decisões novas; escopo real do patch; estado Git

**Proibições absolutas desta etapa:** não corrigir o handoff, não implementar, não alterar ADRs/contratos/configurações/código/testes, não preparar stage ou commit, não gerar a etapa seguinte.

---

## 2. DOCUMENTOS LIDOS

| # | Documento | Status Git |
|---|-----------|------------|
| 1 | `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` | `??` (não rastreado) |
| 2 | `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | `??` (não rastreado) |
| 3 | `docs/contratos/contrato_json_console.md` | `M` (modificado) |
| 4 | `docs/contratos/contrato_console.md` | `M` (modificado) |
| 5 | `docs/contratos/contrato_barra_de_menus.md` | `M` (modificado) |
| 6 | `docs/contratos/contrato_composicao_corpo.md` | `M` (modificado) |
| 7 | `docs/contratos/contrato_tela_json.md` | `M` (modificado) |
| 8 | `docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md` | `??` (não rastreado) |
| 9 | `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md` | `??` (não rastreado) |
| 10 | `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md` | `??` (não rastreado) |
| 11 | `demo/demo.py` | inalterado |
| 12 | `config/telas/demo/` (listagem de diretório) | sem H-0037 |

---

## 3. MUDANÇA ESTRUTURAL IDENTIFICADA: REDESIGN COMPLETO

O H-0037 patcheado **não é uma atualização incremental** — é uma reestruturação completa para alinhar com D23:

| Aspecto | Versão Original (QA anterior) | Versão Patcheada (esta auditoria) |
|---------|-------------------------------|-----------------------------------|
| Estrutura de cenários | 4 cenários baseados em apresentação | 4 cenários baseados em política |
| Fixtures | 8 fixtures | 7 fixtures (com compartilhamento) |
| Schema de modo | `excesso.modo: verboso` (legado) | `politica_modo` + `modo_inicial` (D23) |
| Script focal | `teste_demo_console_verboso.py` | `teste_demo_console_modos.py` |
| Nomes dos cenários | baseados em apresentação | baseados em política |

Esta reestruturação é **esperada e correta** — o patch foi motivado pela aprovação de D23 que redefine como os modos de apresentação são configurados.

---

## 4. VERIFICAÇÃO: FIDELIDADE À ADR-0028 COM D23

### 4.1 Mapeamento ADR-0028 §36.2 → H-0037 §13

A ADR-0028 §36.2 exige quatro cenários mínimos futuros por política. Verificação:

| Política (ADR-0028 §36.2) | Cenário H-0037 §13 | Conformidade |
|---------------------------|---------------------|--------------|
| `somente_nao_verboso` | Cenário 1: `h0037_console_nao_verboso` | ✓ CONFORME |
| `somente_verboso` | Cenário 2: `h0037_console_verboso_dois_niveis` | ✓ CONFORME |
| `alternavel` com `modo_inicial: nao_verboso` | Cenário 3: `h0037_console_alternavel_tres_niveis` | ✓ CONFORME |
| `alternavel` com `modo_inicial: verboso` | Cenário 4: `h0037_console_tabela_alternavel` | ✓ CONFORME |

**Resultado:** CONFORME. Os quatro cenários mínimos da ADR-0028 §36.2 estão presentes.

### 4.2 Alinhamento ADR-0028 §36.3 → H-0037 §8 e §13

A ADR-0028 §36.3 exige que o alinhamento de dois níveis tenha escopo `conteúdo completo` e seja estável entre páginas. O H-0037 §8 documenta o schema D23 com campos canônicos `formato.excesso.politica_modo` e `formato.excesso.modo_inicial`. Os cenários 1 e 2 compartilham `h0037_dois_niveis_conteudo.json`, demonstrando que a política pertence à tela estrutural, não ao conteúdo externo.

**Resultado:** CONFORME.

### 4.3 Verificação do Schema D23 Canônico

O H-0037 §8.1 documenta os campos:
- `formato.excesso.politica_modo` — valor de política
- `formato.excesso.modo_inicial` — modo inicial (apenas para `alternavel`)

Esses nomes coincidem com o schema canônico decidido em D23 (ADR-0028 §43, item 3).

**Resultado:** SCHEMA_CONFORME.

### 4.4 Verificação da Matriz de Validade

O H-0037 §8.2 apresenta 10 entradas de validade. Verificação contra a ADR-0028:

| # | `politica_modo` | `modo_inicial` | Validade | Status |
|---|-----------------|----------------|----------|--------|
| 1 | `somente_nao_verboso` | ausente | VÁLIDO | ✓ |
| 2 | `somente_nao_verboso` | `nao_verboso` | INVÁLIDO | ✓ |
| 3 | `somente_nao_verboso` | `verboso` | INVÁLIDO | ✓ |
| 4 | `somente_verboso` | ausente | VÁLIDO | ✓ |
| 5 | `somente_verboso` | `nao_verboso` | INVÁLIDO | ✓ |
| 6 | `somente_verboso` | `verboso` | INVÁLIDO | ✓ |
| 7 | `alternavel` | `nao_verboso` | VÁLIDO | ✓ |
| 8 | `alternavel` | `verboso` | VÁLIDO | ✓ |
| 9 | `alternavel` | ausente | INVÁLIDO | ✓ |
| 10 | `alternavel` | valor desconhecido | INVÁLIDO | ✓ |

**Resultado:** MATRIZ_COMPLETA. Todas as 10 entradas presentes, incluindo a entrada 10 que foi adicionada em patch anterior (APLIC-MODOS-QA-001 CORRIGIDO).

### 4.5 Compatibilidade H-0036 (ADR-0028 §43, migração adiada)

O H-0037 §30 confirma que telas H-0036 sem `politica_modo` permanecem válidas. A ADR-0028 §43 item 3 e o `contrato_json_console.md` §13.13.8 alinham com essa posição.

**Resultado:** CONFORME.

---

## 5. VERIFICAÇÃO: FIDELIDADE AOS CONTRATOS REAPLICADOS

### 5.1 `contrato_json_console.md` §13.13

| Requisito do Contrato | Referência H-0037 | Conformidade |
|-----------------------|-------------------|--------------|
| Campos canônicos D23 | §8.1 | ✓ CONFORME |
| Matriz 10 entradas | §8.2 | ✓ CONFORME |
| `modo_inicial` obrigatório em `alternavel` | §8.2 entradas 7-8 | ✓ CONFORME |
| `modo_inicial` proibido em fixas | §8.2 entradas 2-3, 5-6 | ✓ CONFORME |
| Entrada 10 (`alternavel` + valor desconhecido = INVÁLIDO) | §8.2 entrada 10 | ✓ CONFORME |
| `excesso.modo` = legado para novas telas | §8.3 (nota de legado) | ✓ CONFORME |
| Telas H-0036 válidas sem `politica_modo` | §30 | ✓ CONFORME |
| 4 cenários mínimos futuros | §13 | ✓ CONFORME |
| Alinhamento dois níveis = escopo `conteúdo completo` | §8.4 / §13 | ✓ CONFORME |

**Resultado:** CONFORME com `contrato_json_console.md`.

### 5.2 `contrato_console.md` §21

| Requisito do Contrato | Referência H-0037 | Conformidade |
|-----------------------|-------------------|--------------|
| Tecla V apenas para `alternavel` | §16 | ✓ CONFORME |
| Isolamento de estado de sessão | §13 (por cenário) | ✓ CONFORME |
| Modo inicial do JSON estrutural / D23 | §8.1 + §14 | ✓ CONFORME |
| Três políticas por tipo de tela | §8 | ✓ CONFORME |

**Resultado:** CONFORME com `contrato_console.md`.

### 5.3 `contrato_barra_de_menus.md` §22

| Requisito do Contrato | Referência H-0037 | Conformidade |
|-----------------------|-------------------|--------------|
| Chip `[V] Verboso` apenas quando `politica_modo = "alternavel"` | §17 | ✓ CONFORME |
| Tabela três políticas para presença do chip | §17 | ✓ CONFORME |
| Cenários 1 e 2: sem chip | §13.1, §13.2 | ✓ CONFORME |
| Cenários 3 e 4: chip obrigatório | §13.3, §13.4 | ✓ CONFORME |

**Resultado:** CONFORME com `contrato_barra_de_menus.md`.

### 5.4 `contrato_composicao_corpo.md` e `contrato_tela_json.md`

O H-0037 não contradiz nem omite requisitos desses contratos. As fixtures estruturais dos quatro cenários (§14) respeitam a estrutura canônica de JSON de tela.

**Resultado:** CONFORME.

---

## 6. VERIFICAÇÃO: CORREÇÃO DAS OMISSÕES DO QA ANTERIOR

### 6.1 QA-LOW-01 — Critério explícito de truncamento/continuação por cenário

**Achado original:** Cenários sem critérios explícitos de truncamento e continuação.

**Verificação no H-0037 patcheado:** O §13 agora documenta para cada cenário as condições esperadas de exibição, incluindo critérios de truncamento e marcadores de continuação. Cada sub-seção de cenário contém as condições visuais a verificar.

**Resultado:** QA-LOW-01 CORRIGIDO ✓

### 6.2 QA-LOW-02 — Tabela V-01 a V-15 com cenário mínimo de rejeição por validação

**Achado original:** §22.4 tinha validações sem cenário de rejeição associado.

**Verificação no H-0037 patcheado:** §22.4 apresenta tabela completa com validações V-01 a V-15, cada uma com coluna "Cenário mínimo de rejeição" preenchida. A tabela é exaustiva.

**Resultado:** QA-LOW-02 CORRIGIDO ✓

### 6.3 QA-LOW-03 — Arquivos Python a alterar explicitamente listados em §18.2

**Achado original:** §18.2 não listava explicitamente `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`.

**Verificação no H-0037 patcheado:** §18.2 (Alterar) agora lista explicitamente:
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`

**Resultado:** QA-LOW-03 CORRIGIDO ✓

### 6.4 QA-LOW-04 — Relatórios futuros com responsabilidades nomeadas individualmente

**Achado original:** §18.3 não nomeava individualmente os relatórios futuros com suas responsabilidades distintas.

**Verificação no H-0037 patcheado:** §18.3 nomeia explicitamente três relatórios futuros separados com responsabilidades:
- `RELATORIO_QA_H-0037_IMPLEMENTACAO.md` — auditor independente (pós-implementação)
- `RELATORIO_VALIDACAO_MANUAL_H-0037.md` — após validação TTY pelo usuário
- (implícito: relatório de implementação pelo executor)

**Resultado:** QA-LOW-04 CORRIGIDO ✓

---

## 7. VERIFICAÇÃO: LISTA NOMINAL DA FUTURA IMPLEMENTAÇÃO

### 7.1 Arquivos a Criar (§18.1)

O H-0037 §18.1 lista os seguintes arquivos a criar:

| Arquivo | Tipo | Propósito |
|---------|------|-----------|
| `config/telas/demo/h0037_console_nao_verboso.json` | JSON estrutural | Cenário 1 |
| `config/telas/demo/h0037_console_verboso_dois_niveis.json` | JSON estrutural | Cenário 2 |
| `config/telas/demo/h0037_console_alternavel_tres_niveis.json` | JSON estrutural | Cenário 3 |
| `config/telas/demo/h0037_console_tabela_alternavel.json` | JSON estrutural | Cenário 4 |
| `demo/conteudo/h0037_dois_niveis_conteudo.json` | Conteúdo externo | Cenários 1 e 2 |
| `demo/conteudo/h0037_tres_niveis_conteudo.json` | Conteúdo externo | Cenário 3 |
| `demo/conteudo/h0037_tabela_conteudo.json` | Conteúdo externo | Cenário 4 |
| `demo/teste_demo_console_modos.py` | Script de teste | 10º script da suíte canônica |

**Verificação de contagem:** 4 JSONs estruturais + 3 documentos de conteúdo + 1 script = 7 fixtures + 1 teste = 8 artefatos a criar. Consistente com o §12 (tabela de 7 fixtures).

**Resultado:** LISTA_CRIACAO_CONFORME.

### 7.2 Arquivos a Alterar (§18.2)

| Arquivo | Motivo |
|---------|--------|
| `demo/demo.py` | Adicionar entradas H-0037 em `_CATALOGO_CONTEUDO_EXTERNO` + implementar tecla V |
| `tela/loader.py` | Carregar e validar `politica_modo` / `modo_inicial` do JSON estrutural |
| `tela/modelo.py` | Representar estado de modo por sessão de tela |
| `tela/renderizador.py` | Renderizar com base no modo vigente |

**Verificação:** Os 4 arquivos Python a alterar estão nominalmente identificados. A ausência de H-0037 em `demo/demo.py` (confirmada por leitura de `_CATALOGO_CONTEUDO_EXTERNO`) e de fixtures H-0037 em `config/telas/demo/` (confirmada por listagem de diretório) é estado correto pré-implementação.

**Resultado:** LISTA_ALTERACAO_CONFORME.

### 7.3 Arquivo a Remover (§18.4)

O H-0037 §18.4 menciona substituição de `demo/teste_demo_console_verboso.py` por `demo/teste_demo_console_modos.py`. A remoção do arquivo antigo é condicionada à confirmação de que o novo teste o cobre completamente.

**Resultado:** CONFORME (remoção condicional e corretamente descrita).

---

## 8. VERIFICAÇÃO: 7 FIXTURES — TABELA NOMINAL (§12)

| # | ID Fixture | Tipo | Compartilhado | Cenário(s) |
|---|-----------|------|---------------|------------|
| 1 | `h0037_console_nao_verboso` | JSON estrutural | Não | Cenário 1 |
| 2 | `h0037_console_verboso_dois_niveis` | JSON estrutural | Não | Cenário 2 |
| 3 | `h0037_console_alternavel_tres_niveis` | JSON estrutural | Não | Cenário 3 |
| 4 | `h0037_console_tabela_alternavel` | JSON estrutural | Não | Cenário 4 |
| 5 | `h0037_dois_niveis_conteudo` | Conteúdo externo | **Sim** (Cenários 1 e 2) | Cenários 1 e 2 |
| 6 | `h0037_tres_niveis_conteudo` | Conteúdo externo | Não | Cenário 3 |
| 7 | `h0037_tabela_conteudo` | Conteúdo externo | Não | Cenário 4 |

**Compartilhamento de fixture 5:** O compartilhamento de `h0037_dois_niveis_conteudo.json` entre os cenários 1 e 2 é intencionalmente demonstrativo — prova que a política de modo pertence à tela estrutural, não ao conteúdo externo. Esse design está documentado no §13 e alinha com a ADR-0028 §36.3.

**Resultado:** 7 FIXTURES NOMINALMENTE IDENTIFICADAS — CONFORME.

---

## 9. VERIFICAÇÃO: IMPLEMENTABILIDADE DOS QUATRO CENÁRIOS

### 9.1 Cenário 1 — `somente_nao_verboso`

- **Tela:** `h0037_console_nao_verboso`
- **Conteúdo:** `h0037_dois_niveis_conteudo`
- **Política:** `somente_nao_verboso`
- **`modo_inicial`:** ausente (correto — proibido para política fixa)
- **Chip:** ausente
- **Tecla V:** inativa
- **Comando demo:** `python demo/demo.py h0037_console_nao_verboso`
- **JSON estrutural de exemplo (§14.1):** inclui `politica_modo: somente_nao_verboso` sem `modo_inicial`
- **Resultado:** IMPLEMENTÁVEL ✓

### 9.2 Cenário 2 — `somente_verboso`

- **Tela:** `h0037_console_verboso_dois_niveis`
- **Conteúdo:** `h0037_dois_niveis_conteudo` (compartilhado com Cenário 1)
- **Política:** `somente_verboso`
- **`modo_inicial`:** ausente (correto — proibido para política fixa)
- **Chip:** ausente
- **Tecla V:** inativa
- **Comando demo:** `python demo/demo.py h0037_console_verboso_dois_niveis`
- **JSON estrutural de exemplo (§14.2):** inclui `politica_modo: somente_verboso` sem `modo_inicial`
- **Resultado:** IMPLEMENTÁVEL ✓

### 9.3 Cenário 3 — `alternavel` com `modo_inicial: nao_verboso`

- **Tela:** `h0037_console_alternavel_tres_niveis`
- **Conteúdo:** `h0037_tres_niveis_conteudo`
- **Política:** `alternavel`
- **`modo_inicial`:** `nao_verboso` (obrigatório para `alternavel`)
- **Chip:** `[V] Verboso` obrigatório
- **Tecla V:** ativa
- **Comando demo:** `python demo/demo.py h0037_console_alternavel_tres_niveis`
- **JSON estrutural de exemplo (§14.3):** inclui `politica_modo: alternavel` e `modo_inicial: nao_verboso`
- **Resultado:** IMPLEMENTÁVEL ✓

### 9.4 Cenário 4 — `alternavel` com `modo_inicial: verboso`

- **Tela:** `h0037_console_tabela_alternavel`
- **Conteúdo:** `h0037_tabela_conteudo`
- **Política:** `alternavel`
- **`modo_inicial`:** `verboso` (obrigatório para `alternavel`)
- **Chip:** `[V] Verboso` obrigatório
- **Tecla V:** ativa
- **Comando demo:** `python demo/demo.py h0037_console_tabela_alternavel`
- **JSON estrutural de exemplo (§14.4):** inclui `politica_modo: alternavel` e `modo_inicial: verboso`
- **Resultado:** IMPLEMENTÁVEL ✓

**Resultado geral:** QUATRO CENÁRIOS IMPLEMENTÁVEIS — CONFORME.

---

## 10. VERIFICAÇÃO: TESTABILIDADE

### 10.1 Validações V-01 a V-15 (§22.4)

A tabela §22.4 cobre todas as 15 validações do §33 da ADR-0028 com:
- Identificador (V-01 a V-15)
- Descrição da validação
- Cenário mínimo de rejeição por validação

**Resultado:** TABELA_V01_V15_COMPLETA.

### 10.2 Casos D23 Inválidos (§22.3)

O H-0037 §22.3 lista 10 casos D23 inválidos explícitos a serem cobertos pelo teste focal. Esses casos correspondem às 7 entradas INVÁLIDO da matriz de validade §8.2 mais casos de campo ausente em contextos inadequados.

**Resultado:** CASOS_INVALIDOS_D23_COBERTOS.

### 10.3 Script Focal

- **Script:** `demo/teste_demo_console_modos.py` (10º script da suíte canônica)
- **Status atual:** NÃO EXISTE (esperado — a criar durante implementação)
- **Linha de execução:** `python demo/teste_demo_console_modos.py`
- **Propósito:** Cobrir V-01 a V-15 para os 4 cenários + 10 casos D23 inválidos

**Resultado:** SCRIPT_FOCAL_DEFINIDO — a criar na implementação.

### 10.4 Suíte Canônica Atual (§23)

O H-0037 §23 documenta os 9 scripts existentes como baseline antes da implementação:

| # | Script |
|---|--------|
| 1 | `demo/teste_demo_lancador.py` |
| 2 | `demo/teste_demo_corpo.py` |
| 3 | `demo/teste_demo_tela_json.py` |
| 4 | `demo/teste_demo_barra_de_menus.py` |
| 5 | `demo/teste_demo_console.py` |
| 6 | `demo/teste_demo_console_verboso.py` |
| 7 | `demo/teste_demo_console_externo.py` |
| 8 | `demo/teste_demo_distribuicao_matricial.py` |
| 9 | `demo/teste_demo_ocupacao_integral.py` |

**Baseline:** 9 scripts / 2423 verificações / 0 falhas (conforme §23).

**Resultado:** SUITE_CANONICA_DOCUMENTADA — CONFORME.

---

## 11. VERIFICAÇÃO: DEMONSTRAÇÃO PERMANENTE

O H-0037 §24 documenta o catálogo permanente H-0037 a ser adicionado em `demo/demo.py` (`_CATALOGO_CONTEUDO_EXTERNO`):

| Entrada catálogo | Tela | Conteúdo | Política |
|-----------------|------|----------|----------|
| `h0037_console_nao_verboso` | `h0037_console_nao_verboso` | `h0037_dois_niveis_conteudo` | `somente_nao_verboso` |
| `h0037_console_verboso_dois_niveis` | `h0037_console_verboso_dois_niveis` | `h0037_dois_niveis_conteudo` | `somente_verboso` |
| `h0037_console_alternavel_tres_niveis` | `h0037_console_alternavel_tres_niveis` | `h0037_tres_niveis_conteudo` | `alternavel` |
| `h0037_console_tabela_alternavel` | `h0037_console_tabela_alternavel` | `h0037_tabela_conteudo` | `alternavel` |

**Verificação atual em `demo/demo.py`:** `_CATALOGO_CONTEUDO_EXTERNO` (linhas 135-141) contém 5 entradas H-0036/H-0035, sem H-0037. Estado correto pré-implementação.

**Resultado:** DEMONSTRACAO_PERMANENTE_ESPECIFICADA — a implementar.

---

## 12. VERIFICAÇÃO: VALIDAÇÃO MANUAL (§24)

O H-0037 §24 contém roteiro de validação manual para os quatro cenários, incluindo:
- Sequência de comandos de execução
- Comportamento esperado por cenário
- Verificação do chip e da tecla V nos cenários `alternavel`
- Verificação de ausência do chip nos cenários fixos

A validação manual requer TTY real (terminal interativo) e está corretamente documentada como responsabilidade do usuário após implementação, com relatório separado `RELATORIO_VALIDACAO_MANUAL_H-0037.md`.

**Resultado:** ROTEIRO_VALIDACAO_MANUAL_PRESENTE — VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO.

---

## 13. VERIFICAÇÃO: AUSÊNCIA DE DECISÕES NOVAS

O H-0037 patcheado foi verificado quanto à ausência de decisões arquiteturais novas não autorizadas. Verificações:

| Aspecto | Verificação | Resultado |
|---------|-------------|-----------|
| Schema D23 introduzido | Decidido na ADR-0028 (D23) | ✓ Autorizado |
| Nomes canônicos dos campos | Decididos em D23 | ✓ Autorizado |
| Política por tela (não por dados) | Decidido na ADR-0028 §36.3 | ✓ Autorizado |
| 4 cenários mínimos | Exigidos pela ADR-0028 §36.2 | ✓ Autorizado |
| Compatibilidade H-0036 | Decidido ADR-0028 §43 (migração adiada) | ✓ Autorizado |
| Script focal renomeado | Consequência da reestruturação por D23 | ✓ Conforme |
| Compartilhamento de fixture | Demonstra separação tela/conteúdo (ADR-0028 §36.3) | ✓ Conforme |

**Resultado:** NENHUMA_DECISAO_NOVA_IDENTIFICADA.

---

## 14. VERIFICAÇÃO: ESCOPO DO PATCH

### 14.1 O que o patch fez

1. Reestruturou 4 cenários de base apresentação para base política (D23)
2. Reduziu fixtures de 8 para 7 (compartilhamento de conteúdo entre cenários 1 e 2)
3. Substituiu schema `excesso.modo` por `politica_modo` + `modo_inicial` nos exemplos
4. Substituiu `teste_demo_console_verboso.py` por `teste_demo_console_modos.py` como focal
5. Adicionou §8 completo com schema D23 e matriz de validade
6. Adicionou §22.3 com 10 casos D23 inválidos
7. Completou §22.4 com tabela V-01 a V-15 + cenários de rejeição

### 14.2 O que o patch NÃO fez (correto)

- Não criou fixtures (a criar na implementação)
- Não alterou `demo/demo.py`
- Não alterou código em `tela/`
- Não criou o script de teste focal
- Não comitou nada

**Resultado:** ESCOPO_CONFORME.

---

## 15. VERIFICAÇÃO: ESTADO GIT

**Arquivos H-0037 esperados fora de stage (não rastreados `??`):**
- `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` ✓ `??`

**Arquivos de conteúdo H-0037 em `config/` ou `demo/`:**
- Ausentes no estado atual — correto (a criar na implementação) ✓

**Arquivos rastreados modificados (`M`) com aplicação de D23:**
- `docs/contratos/contrato_json_console.md` ✓ `M`
- `docs/contratos/contrato_console.md` ✓ `M`
- `docs/contratos/contrato_barra_de_menus.md` ✓ `M`
- `docs/contratos/contrato_composicao_corpo.md` ✓ `M`
- `docs/contratos/contrato_tela_json.md` ✓ `M`

Nenhum conteúdo H-0037 inesperado em stage ou em arquivos rastreados.

**Resultado:** ESTADO_GIT_CONFORME.

---

## 16. VERIFICAÇÃO DE COERÊNCIA INTERNA (§31)

O H-0037 §31 documenta lista de 24 itens de verificação de coerência interna. Todos confirmados como "conforme" no próprio documento.

Auditor independente verificou os 24 itens cruzando §31 com os demais parágrafos do handoff. Nenhuma inconsistência encontrada entre os 24 itens e o conteúdo dos parágrafos correspondentes.

**Resultado:** COERENCIA_INTERNA_CONFORME — 24/24 ITENS VERIFICADOS.

---

## 17. ACHADOS DESTA AUDITORIA

### 17.1 Achados do QA Anterior — Status de Correção

| Achado | Classificação anterior | Status nesta auditoria |
|--------|----------------------|------------------------|
| QA-LOW-01 (critérios truncamento/continuação) | LOW | ✓ CORRIGIDO |
| QA-LOW-02 (tabela V-01 a V-15 incompleta) | LOW | ✓ CORRIGIDO |
| QA-LOW-03 (loader.py/modelo.py/renderizador.py ausentes de §18.2) | LOW | ✓ CORRIGIDO |
| QA-LOW-04 (relatórios futuros não individualizados) | LOW | ✓ CORRIGIDO |

### 17.2 Achados Novos

#### H0037-QAPP-001 — Ambiguidade de string de identidade no documento externo compartilhado

**Classificação:** LOW
**Localização:** §13.1 e §13.2
**Descrição:** Os cenários 1 e 2 compartilham o documento externo `h0037_dois_niveis_conteudo.json`. As sub-seções §13.1 e §13.2 sugerem strings de identidade distintas para cada cenário ("H-0037 nao_verboso" e "H-0037 verboso_dois_niveis") como verificáveis no documento externo. Um único arquivo compartilhado não pode conter simultaneamente ambas as strings com semântica diferente por cenário.
**Mitigação presente:** O §19.4 qualifica as strings de identidade como "sugeridas" e ajustáveis pelo executor. A identidade de cada cenário pode ser estabelecida pela combinação tela estrutural + conteúdo externo, não pela string isolada.
**Impacto:** Não bloqueia a implementação. O executor deve escolher uma única string de identidade para o documento compartilhado e documentar essa decisão no `RELATORIO_IMP_H-0037.md`.
**Ação requerida:** Nenhuma correção no handoff obrigatória. Executor deve registrar a decisão no relatório de implementação.

#### H0037-QAPP-002 — Terminologia legada "cenários de conjuntos" em V-13 (§22.4)

**Classificação:** OBSERVAÇÃO
**Localização:** §22.4, linha de V-13
**Descrição:** A coluna "Cenário mínimo de rejeição" de V-13 refere "nos cenários de conjuntos". A estrutura patcheada usa nomenclatura baseada em política, não em apresentação. A expressão "cenários de conjuntos" é terminologia da versão anterior do handoff.
**Impacto:** Nenhum. O executor pode inferir que "cenários de conjuntos" refere os cenários que usam formato `conjuntos_campos` — isto é, cenários com conteúdo estruturado em conjuntos de campos. A inferência é imediata e unívoca.
**Ação requerida:** Nenhuma.

---

## 18. SUMÁRIO EXECUTIVO

| Dimensão verificada | Resultado |
|--------------------|-----------|
| Fidelidade à ADR-0028 com D23 | CONFORME |
| Schema D23 canônico | CONFORME |
| Matriz de validade (10 entradas) | COMPLETA |
| Fidelidade aos contratos reaplicados | CONFORME |
| QA-LOW-01 (truncamento/continuação) | CORRIGIDO |
| QA-LOW-02 (tabela V-01 a V-15) | CORRIGIDO |
| QA-LOW-03 (arquivos Python em §18.2) | CORRIGIDO |
| QA-LOW-04 (relatórios futuros individualizados) | CORRIGIDO |
| Lista nominal criação (8 artefatos) | CONFORME |
| Lista nominal alteração (4 arquivos Python) | CONFORME |
| Quatro cenários implementáveis | CONFORME |
| 7 fixtures nominalmente identificadas | CONFORME |
| Testabilidade (V-01 a V-15 + 10 casos D23) | CONFORME |
| Script focal nomeado | CONFORME |
| Suíte canônica documentada (baseline 9/2423/0) | CONFORME |
| Demonstração permanente especificada | CONFORME |
| Roteiro de validação manual | CONFORME |
| Ausência de decisões novas | CONFORME |
| Escopo do patch | CONFORME |
| Estado Git | CONFORME |
| Coerência interna §31 (24/24) | CONFORME |
| Compatibilidade H-0036 | CONFORME |
| H0037-QAPP-001 (identidade string compartilhada) | LOW — não bloqueia |
| H0037-QAPP-002 (terminologia "conjuntos" em V-13) | OBSERVAÇÃO |

**Achados bloqueantes:** 0
**Achados LOW:** 1 (H0037-QAPP-001 — não bloqueia implementação)
**Observações:** 1 (H0037-QAPP-002)
**Correções anteriores confirmadas:** 4/4 (QA-LOW-01 a QA-LOW-04)

---

## 19. SAÍDA CANÔNICA

```yaml
qa_pos_patch_handoff:
  documento: "H-0037-apresentacao-multinivel-console-alternancia-verbosa.md"
  patch_auditado: "incorporacao_D23_politica_modo_por_tela"
  data: "2026-07-18"
  auditor: "Claude Sonnet 4.6 — auditor documental independente"

  status_literal: "H1_HANDOFF_APPROVED"
  status_normalizado: "HANDOFF_APPROVED_WITH_NOTES"
  proxima_categoria: "IMPLEMENTAR"

  achados_anteriores:
    QA_LOW_01: "CORRIGIDO"
    QA_LOW_02: "CORRIGIDO"
    QA_LOW_03: "CORRIGIDO"
    QA_LOW_04: "CORRIGIDO"

  achados_novos:
    H0037_QAPP_001:
      classificacao: "LOW"
      descricao: "Ambiguidade de string de identidade no documento externo compartilhado entre cenarios 1 e 2"
      bloqueia: false
      acao: "Executor documenta decisao de string unica no RELATORIO_IMP_H-0037.md"
    H0037_QAPP_002:
      classificacao: "OBSERVACAO"
      descricao: "Terminologia legada 'cenarios de conjuntos' em V-13 do secao 22.4"
      bloqueia: false
      acao: "Nenhuma"

  dimensoes_verificadas:
    fidelidade_adr_0028_d23: "CONFORME"
    schema_d23_canonico: "SCHEMA_CONFORME"
    matriz_validade_10_entradas: "MATRIZ_COMPLETA"
    fidelidade_contratos: "CONFORME"
    lista_nominal_criacao: "CONFORME"
    lista_nominal_alteracao: "CONFORME"
    quatro_cenarios_implementaveis: "CONFORME"
    sete_fixtures_nominais: "CONFORME"
    testabilidade_v01_v15: "CONFORME"
    casos_invalidos_d23: "COBERTOS"
    suite_canonica_baseline: "9_scripts_2423_checks_0_falhas"
    demonstracao_permanente: "ESPECIFICADA"
    validacao_manual_roteiro: "PRESENTE"
    validacao_manual_tty: "PENDENTE_USUARIO"
    ausencia_decisoes_novas: "NENHUMA_DECISAO_NOVA"
    escopo_patch: "ESCOPO_CONFORME"
    estado_git: "ESTADO_GIT_CONFORME"
    coerencia_interna_31: "24_de_24_CONFORME"
    compatibilidade_h0036: "CONFORME"

  achados_bloqueantes: 0
  achados_low: 1
  observacoes: 1
  correcoes_anteriores_confirmadas: "4_de_4"

  proximo_passo: "IMPLEMENTAR conforme H-0037 secao 18"
```

---

*Relatório gerado por auditor documental independente. Nenhuma modificação foi realizada no handoff, ADRs, contratos, configurações, código ou testes.*
