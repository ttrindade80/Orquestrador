---
name: relatorio-qa-pos-patch-02-adr-0030
description: Auditoria documental independente do segundo patch focal da ADR-0030
metadata:
  type: relatorio_qa_pos_patch
  adr: ADR-0030
  patch_auditado: docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
  data: "2026-07-22"
  status: concluido
---

# Relatorio - QA pos Patch 02 da ADR-0030

## 1. Identificacao

| Campo | Valor |
|---|---|
| Relatorio | RELATORIO_QA_POS_PATCH_02_ADR-0030 |
| Tipo | QA documental independente pos segundo patch focal |
| ADR auditada | `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md` |
| Patch auditado | `docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md` |
| Achado auditado | `QA-POS-ADR0030-001` |
| Data | 2026-07-22 |

Esta execucao auditou exclusivamente o tratamento do achado `QA-POS-ADR0030-001`.
O QA pos primeiro patch foi preservado como historico e nao foi reexecutado.

---

## 2. Gate inicial

Comandos executados:

```bash
git status --short --untracked-files=all
git diff --check
git diff --cached --check
```

Resultado observado:

```yaml
arquivo_auditado: docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
metadata_status: proposta
status_no_corpo: proposta
encerramento: DOCUMENTATION_PATCHED_AWAITING_QA
qa_anterior_preservado: true
segundo_patch_preservado: true
stage: VAZIO
git_diff_check: sem_apontamentos
git_diff_cached_check: sem_apontamentos
arquivos_nao_rastreados_presentes:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
  - docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
  - docs/relatorios/RELATORIO_PATCH_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_ADR-0030.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
```

O caminho obrigatorio desta execucao nao existia antes da criacao deste
relatorio:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md
```

---

## 3. Cadeia historica preservada

Arquivos historicos presentes e nao sobrescritos:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
docs/relatorios/RELATORIO_QA_ADR-0030.md
docs/relatorios/RELATORIO_PATCH_ADR-0030.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
```

O relatorio antigo `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md` foi
tratado somente como artefato historico. Nenhum conteudo dele foi reutilizado
como resultado atual.

---

## 4. Autoridade canonica do literal

Fontes conferidas:

```text
config/estilo.json
docs/contratos/contrato_estilo.md
```

Resultado:

```yaml
literal_canonico:
  cor_texto: "padrão"
  cor_fundo: "padrão"
normalizacao_lexical_inventada: false
```

Evidencias:

- `config/estilo.json` usa `"padrão"` nos campos `cor_texto` e `cor_fundo`
  dos presets de chip aplicaveis, incluindo `"Colchete"`.
- `docs/contratos/contrato_estilo.md` define `"padrão"` como nome semantico
  de cor sem diferenciacao visual.
- Nao ha autoridade material ou contratual para substituir o valor por
  `"padrao"` sem acento.

---

## 5. Buscas obrigatorias na ADR

Comandos executados:

```bash
rg -n '"padrao"' docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
rg -n '"padrão"' docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

Resultado:

```yaml
ocorrencias_padrao_sem_acento: 0
ocorrencias_padrao_com_acento:
  - linha: 212
    contexto: tabela_D5_cor_texto
  - linha: 213
    contexto: tabela_D5_cor_fundo
  - linha: 225
    contexto: bloco_yaml_Colchete_cor_texto
  - linha: 226
    contexto: bloco_yaml_Colchete_cor_fundo
  - linha: 234
    contexto: implicacoes_migracao_D5
  - linha: 491
    contexto: compatibilidade_preservacao_aparencia
```

Conclusao: o literal incorreto `"padrao"` nao permanece na ADR; o literal
correto `"padrão"` aparece nas secoes materiais esperadas.

---

## 6. Conferencia material nominal

```yaml
tabela_D5:
  status: conforme
  cor_texto: "padrão"
  cor_fundo: "padrão"
  ausencia_de_cor_concreta_nova: true

bloco_yaml_preset_Colchete:
  status: conforme
  preset_ativo: "Colchete"
  cor_texto: "padrão"
  cor_fundo: "padrão"
  caixa_alta:
    valor_atual_no_arquivo: true
    valor_final_decidido: false

implicacoes_da_migracao:
  status: conforme
  caixa_alta_final: false
  cor_texto_e_cor_fundo_nao_introduzem_cor_concreta: true

compatibilidade:
  status: conforme
  borda: "Borda Curva"
  chip: "Colchete"
  cor_texto: "padrão"
  cor_fundo: "padrão"
  caixa_alta_final: false

relatorio_do_segundo_patch:
  status: conforme
  achado: QA-POS-ADR0030-001
  status_achado_no_patch: TRATADO
  valor_anterior: "padrao"
  valor_correto: "padrão"
  substituicoes: 10
  linhas_afetadas: 6
  decisoes_semanticas_alteradas: false

preservacao_caixa_alta_false:
  status: conforme
  evidencia: D5, compatibilidade e criterios_de_migracao preservam valor_final_decidido false

ausencia_de_valores_concretos_novos_de_cor:
  status: conforme
  evidencia: a ADR declara que "padrão" nao introduz nova cor concreta
```

---

## 7. Regressao

Itens conferidos como preservados:

```yaml
D1_a_D13: preservadas
preset_borda: "Borda Curva"
preset_chip: "Colchete"
caixa_alta_final: false
preset_cursor: "Seta"
preset_inclusao: "Círculo"
fallback_silencioso: proibido
tipo_borda_no_estado_final: ausente
tela_de_estilo: deferida
Bloco_2: fora_do_escopo
Bloco_3: fora_do_escopo
ordem_futura_dos_chips: preservada
matriz_de_propagacao: preservada
status_ADR: proposta
```

Nao foi identificada alteracao indevida em:

```yaml
genealogia: preservada
aplicacao_documental_versus_implementacao: preservada
validacoes_de_caractere: preservadas
duplicidade_raw: preservada
decisoes_deferidas: preservadas
rastreabilidade: preservada
encerramento: preservado
```

---

## 8. Classificacao do achado auditado

```yaml
id: QA-POS-ADR0030-001
status: RESOLVIDO
evidencia:
  - ausencia_total_de_ocorrencias_de_padrao_sem_acento_na_ADR
  - presenca_de_padrao_com_acento_nas_secoes_materiais_D5_migracao_e_compatibilidade
  - alinhamento_com_config_estilo_json
  - alinhamento_com_contrato_estilo_md
regressao_introduzida: false
impacto: divergencia_literal_sanada_sem_alteracao_semantica
```

---

## 9. Achados novos

```yaml
achados_novos: []
```

Nenhum achado novo com impacto factual, normativo ou operacional real foi
identificado nesta auditoria.

---

## 10. Checks finais

Comandos previstos para encerramento:

```bash
git status --short --untracked-files=all
git diff --check
git diff --cached --check
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Resultado dos checks finais:

```yaml
git_status_final:
  stage: VAZIO
  arquivos_nao_rastreados_presentes:
    - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md
    - docs/relatorios/RELATORIO_PATCH_02_ADR-0030.md
    - docs/relatorios/RELATORIO_PATCH_ADR-0030.md
    - docs/relatorios/RELATORIO_QA_ADR-0030.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_02_ADR-0030.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0030.md
git_diff_check_final: sem_apontamentos
git_diff_cached_check_final: sem_apontamentos
pytest_final:
  status: passou
  total: 422
```

---

## 11. Parecer final

```yaml
QA_POS_PATCH_02_ADR_0030: APROVADO
achado_original: QA-POS-ADR0030-001
status_achado_original: RESOLVIDO
regressoes: false
achados_novos: []
encerramento: QA_POS_PATCH_02_APROVADO
```

QA_POS_PATCH_02_APROVADO
