# Relatório de Patch de Consistência Documental — Ciclo ADR-0030 / H-0039

```yaml
arquivo_correto: docs/relatorios/RELATORIO_PATCH_CONSISTENCIA_DOCUMENTAL_CICLO_ADR-0030_H-0039.md
etapa_correta: PATCH_CONSISTENCIA_DOCUMENTAL
ciclo:
  adr: ADR-0030
  handoff: H-0039
  bloco: 1
status_final: DOCUMENTATION_CONSISTENCY_PATCH_COMPLETED
proxima_categoria: QA_POS_PATCH_CONSISTENCIA
```

## 1. Identificação

| Campo | Valor |
|---|---|
| Etapa | PATCH_CONSISTENCIA_DOCUMENTAL |
| ADR | ADR-0030 |
| Handoff | H-0039 |
| Bloco | 1 |
| Data de execução | 2026-07-22 |
| Executor | Claude Code |

---

## 2. Relatório de consistência de origem

```yaml
relatorio_origem: docs/relatorios/RELATORIO_CONSISTENCIA_DOCUMENTAL_CICLO_ADR-0030_H-0039.md
status_origem: DOCUMENTATION_CONSISTENCY_PATCH_REQUIRED
achados_para_tratamento:
  - CD-ADR0030-H0039-001  # severidade: alta
  - CD-ADR0030-H0039-002  # severidade: media
  - CD-ADR0030-H0039-003  # severidade: baixa
achados_preservados_como_observacao:
  - CD-ADR0030-H0039-004
  - CD-ADR0030-H0039-005
observacao:
  - OBS-H0039-001
```

---

## 3. Arquivos autorizados

Alterados:

```text
docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_estilo.md
```

Criado:

```text
docs/relatorios/RELATORIO_PATCH_CONSISTENCIA_DOCUMENTAL_CICLO_ADR-0030_H-0039.md
```

Não foram alterados nenhum outro arquivo.

---

## 4. Estado anterior (pré-patch)

### ADR-0030

- §2 (Status): declarava QA da aplicação documental pendente e configuração /
  implementação não realizadas — sem distinção entre estado histórico e estado
  atual pós H-0039.
- §11 (Validações): todos os 12 critérios do Bloco 1 marcados como `[ ]`
  (não concluídos).
- §15 (Encerramento):
  ```yaml
  qa_da_aplicacao: PENDENTE
  configuracao_executavel_migrada: false
  implementacao_executada: false
  proxima_categoria: QA_APLICACAO_ADR
  ```
  Última linha: `APLICACAO_ADR_CONCLUIDA_AGUARDANDO_QA`.

### INDICE_ADR.md

- Linha 60 (descrição do ADR-0030): registrava "remoção futura de hardcodings"
  e "QA da aplicação documental pendente" — ambas as afirmações desatualizadas
  após o H-0039.

### contrato_estilo.md

- §3.1 (linha 111–115): usava a formulação "renderer atual" para
  `_BORDAS["curva"]`, que já foi removido do renderer vigente pelo H-0039.
- §3.7 (linhas 295–314): listava decisões do Bloco 1 como "não foram
  realizadas nesta aplicação documental" sem ressalva de que o ciclo posterior
  H-0039 as implementou.

---

## 5. Tratamento de cada achado

### CD-ADR0030-H0039-001 — ADR-0030 com estado ativo desatualizado

**Arquivo:** `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md`

**Seções corrigidas:**

#### §2 Status

- Estado histórico da aplicação documental identificado explicitamente como
  tal (QA pendente naquele momento; migração e implementação ainda não
  realizadas naquele ciclo).
- Adicionado bloco "Estado atual do ciclo" (pós H-0039) com:
  ```yaml
  ADR: aceita
  aplicacao_documental: aprovada
  handoff: H1_HANDOFF_APPROVED
  implementacao: I1_IMPLEMENTATION_APPROVED
  validacao_manual: VALIDACAO_MANUAL_APROVADA
  Bloco_1: concluido
  Bloco_2: futuro
  Bloco_3: futuro
  ```

#### §11 Critérios do Bloco 1

- Todos os 12 critérios originais marcados como `[x]` (concluídos).
- Adicionados três critérios finais também marcados como concluídos:
  - Suíte canônica: `423 passed`.
  - QA técnico: `I1_IMPLEMENTATION_APPROVED`.
  - Validação manual: `VALIDACAO_MANUAL_APROVADA`.

#### §15 Encerramento

- Substituído o bloco com `configuracao_executavel_migrada: false` e
  `implementacao_executada: false` pelo bloco factual atual:
  ```yaml
  qa_da_aplicacao: ADR_APPLICATION_APPROVED
  configuracao_executavel_migrada: true
  implementacao_Bloco_1_executada: true
  QA_tecnico: I1_IMPLEMENTATION_APPROVED
  validacao_manual: VALIDACAO_MANUAL_APROVADA
  patch_implementacao_necessario: false
  Bloco_1_concluido: true
  Bloco_2_concluido: false
  Bloco_3_concluido: false
  consistencia_documental_pos_ciclo:
    estado: PATCH_EXECUTADO_AGUARDANDO_QA
  ```
- Última linha substituída para `DOCUMENTATION_CONSISTENCY_PATCHED_AWAITING_QA`.
- Ciclo Git não declarado fechado.

---

### CD-ADR0030-H0039-002 — INDICE_ADR.md com descrição desatualizada

**Arquivo:** `docs/adr/INDICE_ADR.md`

**Linha corrigida:** 60

- Removidas as expressões "remoção futura de hardcodings" e "QA da aplicação
  documental pendente".
- Preservados: número, status `aceita`, data `2026-07-22`, título.
- Descrição atualizada para refletir:
  - aplicação documental aprovada em 2026-07-22;
  - Bloco 1 implementado pelo H-0039 (carregamento global e materialização em
    runtime, hardcodings de borda e chip do escopo removidos, validação manual
    aprovada);
  - Blocos 2 e 3 futuros.

---

### CD-ADR0030-H0039-003 — contrato_estilo.md com formulação ativa pré-H-0039

**Arquivo:** `docs/contratos/contrato_estilo.md`

**Seções corrigidas:**

#### §3.1 (Borda — Preservação visual inicial)

- Removida a formulação ativa que apresentava `_BORDAS["curva"]` como estado
  do "renderer atual".
- Substituída por descrição normativa atual:
  - a correspondência com `_BORDAS["curva"]` é identificada como estado
    histórico ("renderer anterior ao H-0039, estado histórico");
  - o renderer vigente recebe o estilo global já resolvido;
  - os sete campos de borda vêm de `EstiloResolvido`;
  - o renderer não mantém catálogo próprio nem escolhe preset;
  - `_BORDAS` e `tipo_borda` não pertencem ao estado executável vigente.

#### §3.7 (Fronteira com implementação)

- Preservada a afirmação histórica de que a aplicação documental da ADR-0030,
  isoladamente, não implementou código.
- A lista de decisões não realizadas naquele momento permanece intacta como
  registro histórico, com rótulo explícito "Na aplicação documental da
  ADR-0030 (estado histórico)".
- Adicionada distinção temporal com bloco yaml:
  ```yaml
  aplicacao_documental_ADR_0030:
    implementacao_executada_naquela_etapa: false

  ciclo_posterior_H_0039:
    carregamento_global: implementado
    materializacao_runtime: implementada
    renderer_migrado: true
    hardcodings_do_escopo_removidos: true
  ```
- Listadas explicitamente as pendências que continuam fora do estado
  implementado: tela de escolha, persistência, troca durante sessão,
  `cor_inativo`, `cor_alerta`, `tiling`, Blocos 2 e 3, promoção de
  `_meta.status`.

---

## 6. Seções alteradas

| Arquivo | Seção | Natureza da alteração |
|---|---|---|
| ADR-0030 | §2 Status | Estado histórico identificado; estado atual pós-H-0039 adicionado |
| ADR-0030 | §11 Critérios do Bloco 1 | Todos os critérios marcados como `[x]`; três itens adicionados |
| ADR-0030 | §15 Encerramento | Bloco yaml substituído; última linha substituída |
| INDICE_ADR.md | Linha 60 | Descrição do ADR-0030 atualizada |
| contrato_estilo.md | §3.1 (linhas 111–117) | Formulação de `_BORDAS["curva"]` como "renderer atual" substituída |
| contrato_estilo.md | §3.7 (linhas 295–341) | Distinção temporal adicionada; pendências futuras listadas |

---

## 7. Distinção entre estado histórico e atual

| Documento | Estado histórico preservado | Estado atual adicionado |
|---|---|---|
| ADR-0030 §2 | "Estado no momento da aplicação documental (histórico)" | Bloco yaml com estado pós-H-0039 |
| ADR-0030 §15 | — (substituído por estado factual) | Bloco completo com `Bloco_1_concluido: true` |
| contrato_estilo.md §3.1 | `_BORDAS["curva"]` identificado como "renderer anterior ao H-0039, estado histórico" | Descrição normativa do renderer vigente |
| contrato_estilo.md §3.7 | Lista de decisões com rótulo "(estado histórico)" | Bloco yaml `ciclo_posterior_H_0039` |

---

## 8. Itens preservados

- Estado histórico da aplicação documental (QA pendente, implementação não
  executada naquele ciclo) — mantido em todos os documentos com identificação
  explícita como estado histórico.
- Rastreabilidade das decisões D4, D5, etc. na ADR-0030 — seções §3.2, §5,
  §9 e §13 não foram alteradas.
- Tabelas de correspondência entre hardcodings históricos e presets — mantidas
  como evidência de decisão.
- Todos os relatórios históricos: RELATORIO_APLICACAO_ADR-0030.md,
  RELATORIO_QA_APLICACAO_ADR-0030.md, RELATORIO_IMPLEMENTACAO_H-0039.md,
  RELATORIO_QA_H-0039_IMPLEMENTACAO.md, RELATORIO_VALIDACAO_MANUAL_H-0039.md
  e demais — não foram alterados.
- H-0039 — não alterado.
- Módulos de nomenclatura — não alterados.
- Código, configuração e testes — não alterados.
- Critérios não concluídos (Bloco 2, Bloco 3, tela de escolha, persistência,
  `cor_inativo`, `cor_alerta`, `tiling`, promoção de `_meta.status`) — não
  marcados como concluídos.

---

## 9. Observações não tratadas (não obrigatórias)

### CD-ADR0030-H0039-004

```yaml
id: CD-ADR0030-H0039-004
severidade: observacao
tema: residuos_textuais_obsoletos_nao_ativos
arquivos: "demo/demo.py; tela/teste_renderizador.py; demo/teste_demo.py; tela/renderizador.py"
motivo_de_preservacao: correcao_nao_obrigatoria
impacto: nenhum_impacto_funcional
```

Resíduos de `tipo_borda`, `_BORDAS` e alternância de borda em comentários,
docstrings, nomes de testes ou testes de ausência. Não contradizem a
documentação normativa vigente. Preservados como nota histórica não
bloqueante conforme OBS-H0039-001.

### CD-ADR0030-H0039-005

```yaml
id: CD-ADR0030-H0039-005
severidade: observacao
tema: suite_focal_no_relatorio_de_implementacao
arquivo: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md
motivo_de_preservacao: correcao_retroativa_nao_obrigatoria
```

Divergência entre suite focal `312/312` no relatório de implementação e
`383/383` no QA técnico. O resultado canônico de QA está preservado; o
relatório de implementação pode ter registrado a suite focal executada naquele
momento. Não exige patch retroativo.

### OBS-H0039-001

```yaml
id: OBS-H0039-001
tema: residuos_textuais_obsoletos_nao_ativos
impacto_funcional: nenhum
bloqueia_consistencia: false
```

Preservada como observação não bloqueante.

---

## 10. Arquivos alterados

```text
docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_estilo.md
docs/relatorios/RELATORIO_PATCH_CONSISTENCIA_DOCUMENTAL_CICLO_ADR-0030_H-0039.md  (criado)
```

---

## 11. Checks

### Busca focal pós-patch

Comando executado:

```bash
rg -n \
  'QA da aplicação.*pendente|QA_da_aplicacao.*pendente|implementacao_executada: false|configuracao_executavel_migrada: false|_BORDAS\["curva"\]|remoção futura de hardcodings|remocao futura de hardcodings|Bloco_1_concluido' \
  docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md \
  docs/adr/INDICE_ADR.md \
  docs/contratos/contrato_estilo.md
```

Ocorrências encontradas e classificadas:

| Arquivo | Linha | Padrão | Classificação |
|---|---|---|---|
| `contrato_estilo.md:113` | `_BORDAS["curva"]` | HISTORICA_E_IDENTIFICADA (marcada como "renderer anterior ao H-0039, estado histórico") |
| `ADR-0030:124` | `_BORDAS["curva"]` | HISTORICA_E_IDENTIFICADA (tabela §3.2 — correspondência de levantamento, evidência de decisão) |
| `ADR-0030:203` | `_BORDAS["curva"]` | HISTORICA_E_IDENTIFICADA (tabela D4 §5 — rationale da escolha do preset) |
| `ADR-0030:513` | `_BORDAS["curva"]` | HISTORICA_E_IDENTIFICADA (§9.1 — argumento histórico de preservação de aparência) |
| `ADR-0030:672` | `_BORDAS["curva"]` | HISTORICA_E_IDENTIFICADA (§13.2 `evidencia_do_levantamento` — genealogia da decisão) |
| `ADR-0030:755` | `Bloco_1_concluido: true` | ATIVA_E_CONFORME (valor correto inserido no §15) |

```yaml
ocorrencias_ativas_desatualizadas: 0
```

### Git checks

```bash
git status --short --untracked-files=all  # ADR-0030 não rastreada; INDICE e contrato: M
git diff --name-only                       # docs/adr/INDICE_ADR.md; docs/contratos/contrato_estilo.md
git diff --check                           # sem erros de whitespace
git diff --cached --name-only              # (vazio — stage limpo)
git diff --cached --check                  # sem erros
```

Resultado:

```yaml
stage: VAZIO
git_diff_check: sem_erros
git_diff_cached_check: sem_erros
adr_0030_status: nao_rastreada_modificada_por_edicao
indice_adr_status: modificado
contrato_estilo_status: modificado
```

---

## 12. Estado Git

```yaml
raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
HEAD: "2caf036 test: adota pytest como padrao unico"
stage: VAZIO
fechamento_git: ausente
arquivos_staged: nenhum
```

Nenhum arquivo foi staged, commitado ou empurrado nesta etapa.

---

## 13. Matriz de achados

| Achado | Arquivo | Estado anterior | Correção | Resultado |
|---|---|---|---|---|
| CD-ADR0030-H0039-001 | `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md` | §2 sem distinção histórico/atual; §11 com todos `[ ]`; §15 com `implementacao_executada: false` | §2: estado histórico identificado + estado atual adicionado; §11: todos `[x]` + 3 itens adicionais; §15: bloco factual atual substituído | TRATADO |
| CD-ADR0030-H0039-002 | `docs/adr/INDICE_ADR.md` | Linha 60 com "remoção futura de hardcodings" e "QA da aplicação documental pendente" | Descrição atualizada: aplicação aprovada, Bloco 1 implementado pelo H-0039, Blocos 2 e 3 futuros | TRATADO |
| CD-ADR0030-H0039-003 | `docs/contratos/contrato_estilo.md` | §3.1 com `_BORDAS["curva"]` como "renderer atual"; §3.7 sem distinção temporal | §3.1: referência histórica identificada + descrição normativa vigente; §3.7: distinção temporal com bloco yaml | TRATADO |
| CD-ADR0030-H0039-004 | `demo/demo.py` etc. | Resíduos textuais em comentários e docstrings | Não corrigido — observação não obrigatória | PRESERVADO_COMO_OBSERVACAO |
| CD-ADR0030-H0039-005 | `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md` | Suite focal 312 vs 383 no QA técnico | Não corrigido — observação não obrigatória | PRESERVADO_COMO_OBSERVACAO |

---

## 14. Resultado factual

```yaml
CD-ADR0030-H0039-001: TRATADO
CD-ADR0030-H0039-002: TRATADO
CD-ADR0030-H0039-003: TRATADO
CD-ADR0030-H0039-004: PRESERVADO_COMO_OBSERVACAO
CD-ADR0030-H0039-005: PRESERVADO_COMO_OBSERVACAO
decisao_do_usuario_necessaria: false
alteracao_semantica_nova: false
ocorrencias_ativas_desatualizadas: 0
stage: VAZIO
outros_arquivos_alterados: nenhum
resultado_factual: DOCUMENTATION_CONSISTENCY_PATCH_COMPLETED
proxima_categoria: QA_POS_PATCH_CONSISTENCIA
```

---

## 15. Encerramento

```yaml
etapa: PATCH_CONSISTENCIA_DOCUMENTAL
ciclo:
  adr: ADR-0030
  handoff: H-0039

arquivos_alterados:
  - docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_estilo.md

relatorio_criado: docs/relatorios/RELATORIO_PATCH_CONSISTENCIA_DOCUMENTAL_CICLO_ADR-0030_H-0039.md

achados_tratados:
  - CD-ADR0030-H0039-001
  - CD-ADR0030-H0039-002
  - CD-ADR0030-H0039-003

observacoes_preservadas:
  - CD-ADR0030-H0039-004
  - CD-ADR0030-H0039-005

ocorrencias_ativas_desatualizadas: 0
outros_arquivos_alterados: nenhum
stage: VAZIO
resultado_factual: DOCUMENTATION_CONSISTENCY_PATCH_COMPLETED
proxima_categoria: QA_POS_PATCH_CONSISTENCIA
encerramento: DOCUMENTATION_CONSISTENCY_PATCHED_AWAITING_QA
```

DOCUMENTATION_CONSISTENCY_PATCHED_AWAITING_QA
