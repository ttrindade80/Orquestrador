---
name: relatorio-patch-02-adr-0030
description: Relatório do segundo patch focal da ADR-0030 — correção do valor literal "padrao" para "padrão" nos campos cor_texto e cor_fundo
metadata:
  type: relatorio_patch
  adr: ADR-0030
  patch_sequencia: 2
  data: "2026-07-22"
---

# Relatório — Segundo Patch Focal da ADR-0030

## 1. Identificação

| Campo | Valor |
|---|---|
| Relatório | RELATORIO_PATCH_02_ADR-0030 |
| Tipo | Patch documental focal |
| ADR alvo | ADR-0030 |
| Sequência | Patch 2 (pós QA-pós-Patch-1) |
| Data | 2026-07-22 |
| Executor | Autor documental — segunda etapa de correção |

---

## 2. Artefato corrigido

```text
docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

---

## 3. QA que originou a correção

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
```

O QA pós-patch identificou que o primeiro patch (RELATORIO_PATCH_ADR-0030.md) não havia corrigido o valor literal de `cor_texto` e `cor_fundo` na ADR-0030. O arquivo de configuração material (`config/estilo.json`) e o contrato (`contrato_estilo.md`) usam o literal `"padrão"` (com acento), mas a ADR usava `"padrao"` (sem acento), sem que existisse qualquer decisão de normalização que justificasse a supressão do acento.

---

## 4. Achado tratado

```yaml
achado: QA-POS-ADR0030-001
status: TRATADO
valor_anterior: "padrao"
valor_correto: "padrão"
natureza: correcao_literal_sem_alteracao_semantica
decisao_do_usuario_necessaria: false
```

**Fundamentação:** O literal `"padrão"` é o valor canônico presente em `config/estilo.json` e em `contrato_estilo.md`. A ADR deve referenciar o literal exato do artefato material e contratual. Não existe decisão de normalização que autorize a supressão do acento.

---

## 5. Autoridade material e contratual

| Fonte | Valor usado | Papel |
|---|---|---|
| `config/estilo.json` | `"padrão"` | Artefato material de configuração |
| `docs/contratos/contrato_estilo.md` | `"padrão"` | Contrato normativo |
| ADR-0030 (antes do patch) | `"padrao"` | Divergência sem decisão de normalização — corrigida |

---

## 6. Ocorrências corrigidas

| Linha (antes do patch) | Localização na ADR | Substituição |
|---|---|---|
| 212 | Tabela D5 — campo `cor_texto` (coluna "Valor em `config/estilo.json`" e coluna "Análise") | `"padrao"` → `"padrão"` (2 ocorrências na linha) |
| 213 | Tabela D5 — campo `cor_fundo` (coluna "Valor em `config/estilo.json`" e coluna "Análise") | `"padrao"` → `"padrão"` (2 ocorrências na linha) |
| 225 | Bloco YAML do preset "Colchete" — campo `cor_texto` | `"padrao"` → `"padrão"` |
| 226 | Bloco YAML do preset "Colchete" — campo `cor_fundo` | `"padrao"` → `"padrão"` |
| 234 | Implicações para a migração (D5) | `"padrao"` → `"padrão"` (2 ocorrências na linha) |
| 491 | Seção 9.1 — Preservação da aparência inicial | `"padrao"` → `"padrão"` (2 ocorrências na linha) |

**Total de substituições:** 10 ocorrências do literal `"padrao"` → `"padrão"` em 6 linhas.

---

## 7. Decisões preservadas

Todas as decisões D1 a D13 foram preservadas integralmente, incluindo:

- `metadata.status: proposta`
- Status da seção 2 como `proposta`
- `"Borda Curva"` como preset ativo de borda
- `"Colchete"` como preset ativo de chip
- `caixa_alta: false` como valor decidido
- `"Seta"` como preset de cursor
- `"Círculo"` como preset de inclusão
- Separação dos três blocos funcionais
- Matriz de propagação documental (seção 14)
- Decisões deferidas (seção 12)
- Ordem futura dos chips
- Proibição de fallback silencioso (D9)
- Estado final sem `tipo_borda`
- Rastreabilidade (seção 13) intocada
- Toda a cadeia histórica de relatórios

Não foi introduzida nenhuma decisão de normalização lexical para `"padrao"`.

As expressões `padrão canônico`, `estilo padrão` e `restauração do padrão` não foram alteradas — a correção incidiu exclusivamente sobre o **valor literal semântico de cor** associado a `cor_texto` e `cor_fundo`.

---

## 8. Arquivos alterados e criados

### Arquivos alterados (preexistentes)

```text
docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

### Arquivos criados

```text
docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
```

### Arquivos históricos preservados (não alterados)

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
docs/relatorios/RELATORIO_QA_ADR-0030.md
docs/relatorios/RELATORIO_PATCH_ADR-0030.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
```

---

## 9. Checks mecânicos

### Verificação de ausência do literal incorreto

```
rg -n '"padrao"' docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

**Resultado:** sem saída — nenhuma ocorrência do literal incorreto permanece.

### Verificação do literal correto

```
rg -n '"padrão"' docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

**Resultado:** 6 linhas com o literal correto `"padrão"`, todas associadas a `cor_texto` ou `cor_fundo`.

### Integridade do diff

```
git diff --check
git diff --cached --check
```

**Resultado:** sem apontamentos de whitespace ou formatação.

---

## 10. Estado Git

```yaml
stage: vazio
arquivos_modificados_fora_do_stage:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md  # untracked, modificado
arquivos_criados_fora_do_stage:
  - docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md  # untracked, criado
commit_realizado: false
push_realizado: false
```

Nenhum relatório histórico foi alterado. Somente a ADR e o presente relatório foram afetados nesta etapa.

---

## 11. Bloqueios

Nenhum bloqueio identificado. A correção é puramente lexical, sem dependência de decisão do usuário, sem conflito com contratos ou com decisões da ADR.

---

## 12. Encerramento

```yaml
achado: QA-POS-ADR0030-001
status: TRATADO
valor_anterior: "padrao"
valor_correto: "padrão"
natureza: correcao_literal_sem_alteracao_semantica
decisao_do_usuario_necessaria: false
```

A ADR-0030 permanece com:

```text
metadata.status: proposta
```

A última linha da ADR permanece:

```text
DOCUMENTATION_PATCHED_AWAITING_QA
```

DOCUMENTATION_PATCHED_AWAITING_QA
