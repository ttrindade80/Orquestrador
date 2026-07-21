# Relatório de QA pós-patch da aplicação — ADR-0029 — fase 2

## 1. Identificação

```yaml
etapa_executada: QA_POS_PATCH_APLICACAO_ADR_FASE_2
fase_auditada: FASE_2_MIGRACAO_DEFINITIVA
data_auditoria: 2026-07-21
auditor: Codex
escopo: auditoria_documental_independente_pos_patch
arquivo_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0029_FASE-2.md
```

## 2. Objetivo e limites

Esta auditoria verificou exclusivamente o tratamento pós-patch dos três achados do QA inicial da aplicação da ADR-0029 fase 2: `QA-F2-001`, `QA-F2-002` e `QA-F2-003`.

Limites observados: não foi refeita auditoria integral da fase 2; não foram corrigidos artefatos auditados; não foram alterados relatórios anteriores; não foi feito stage; não foi feito commit; não foi executada a próxima categoria.

## 3. QA de origem

```yaml
arquivo: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md
status_literal_confirmado: APLICACAO_ADR_FASE_2_REJECTED
proxima_categoria_confirmada: PATCH_APLICACAO_ADR_FASE_2
achados_corretivos_confirmados: 3
achados:
  - QA-F2-001
  - QA-F2-002
  - QA-F2-003
relatorio_QA_inicial_preservado: true
relatorio_QA_inicial_alterado: false
relatorio_QA_pos_patch_separado: true
```

O relatório de QA inicial permanece como relatório rejeitado da etapa anterior e não foi reutilizado como relatório pós-patch.

## 4. Autoridades consultadas

Leitura integral:

| Documento | Uso |
| --------- | --- |
| `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md` | QA inicial rejeitado e achados de origem |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md` | Relatório de aplicação e seção 22 do patch |
| `docs/build_docs/instruction.md` | Evidência de correção de `QA-F2-001` |
| `docs/build_docs/prompts.md` | Evidência de correção de `QA-F2-001` |
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | Evidência de correção de `QA-F2-002` |
| `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | Evidência de correção de `QA-F2-002` |
| `docs/adr/INDICE_ADR.md` | Evidência de correção de `QA-F2-003` |

Consulta seletiva de referência:

| Documento | Uso |
| --------- | --- |
| `docs/NOMENCLATURA.md` | Papel atual da fachada |
| `docs/nomenclatura/00_INDICE.md` | Papel de roteador sem propriedade de definições |
| `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md` | Estado da ADR e categoria de QA |
| `docs/build_docs/to_do.md` | Confirmação focal de não alteração no patch |

## 5. Estado factual do patch

```yaml
patch:
  etapa: PATCH_APLICACAO_ADR_FASE_2
  status_literal: APLICACAO_ADR_FASE_2_CORRIGIDA_AGUARDANDO_QA_POS_PATCH
  proxima_categoria: QA_POS_PATCH_APLICACAO_ADR_FASE_2

QA_origem:
  arquivo: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md
  status_literal: APLICACAO_ADR_FASE_2_REJECTED
  achados_corretivos: 3

arquivos_alterados_no_patch:
  - docs/build_docs/instruction.md
  - docs/build_docs/prompts.md
  - docs/nomenclatura/01_NUCLEO_COMUM.md
  - docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
  - docs/adr/INDICE_ADR.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md

QA_pos_patch_executado_antes_desta_etapa: false
stage_vazio: true
commit_executado: false
```

Nota de rastreabilidade: os seis arquivos do patch foram confirmados pela seção 22 do relatório de aplicação. O working tree contém mudanças acumuladas da ADR-0029 e fases anteriores; portanto, o diff Git físico não isola sozinho o intervalo do patch.

## 6. Auditoria de QA-F2-001

Achado original: `docs/build_docs/instruction.md` e `docs/build_docs/prompts.md` ainda orientavam sessões operacionais a usar o antigo monólito ou suas seções como fonte normativa ativa.

| Arquivo | Ocorrência | Classificação | Autoridade indicada | Resultado |
| ------- | ---------- | ------------- | ------------------- | --------- |
| `docs/build_docs/instruction.md` | linha 15: `docs/NOMENCLATURA.md` listado como fachada no escopo da pasta | FACHADA_DE_NAVEGACAO | módulos em `docs/nomenclatura/`, ADRs, contratos e configs conforme atividade | CONFORME |
| `docs/build_docs/instruction.md` | linha 80: "nunca lê" `docs/NOMENCLATURA.md` durante extração do legado | INSTRUCAO_RESTRITIVA | legado por evidência de código; sem artefatos do sistema novo | CONFORME |
| `docs/build_docs/instruction.md` | linha 112: "Não ler nem citar" `docs/NOMENCLATURA.md` no modelo de prompt | INSTRUCAO_RESTRITIVA | legado por evidência de código; sem artefatos do sistema novo | CONFORME |
| `docs/build_docs/prompts.md` | linha 83: `docs/NOMENCLATURA.md` como fachada de navegação | FACHADA_DE_NAVEGACAO | módulo proprietário localizado via `docs/nomenclatura/00_INDICE.md` | CONFORME |

Critérios avaliados:

| Critério | Resultado |
| -------- | --------- |
| `docs/NOMENCLATURA.md` aparece somente como fachada ou restrição | CONFORME |
| Nenhuma seção numerada antiga indicada como autoridade vigente | CONFORME |
| Decisões e nomes direcionados para módulos proprietários | CONFORME |
| Roteamento por `docs/nomenclatura/00_INDICE.md` quando o módulo não é conhecido | CONFORME |
| Fluxo por contrato, artefato ou atividade | CONFORME |
| Ausência de exigência de leitura dos 17 módulos | CONFORME |
| `00_INDICE.md` não promovido a proprietário de definições | CONFORME |
| Objetivo operacional dos documentos preservado | CONFORME |

Resultado do achado: `RESOLVIDO`.

## 7. Auditoria de QA-F2-002

Achado original: os módulos `01` e `02` ainda permitiam interpretar `docs/NOMENCLATURA.md` como autoridade atual de schema ou semântica.

| Módulo | Trecho sobre o monólito | Marcador histórico | Papel atual da fachada explícito | Ambiguidade restante | Resultado |
| ------ | ----------------------- | ------------------ | -------------------------------- | -------------------- | --------- |
| `01_NUCLEO_COMUM.md` | linhas 81-86: responsabilidade antiga do monólito, substituído pela fachada na fase 2 | "antigo monólito", "substituído pela fachada" | "A autoridade vigente deste domínio é o presente módulo"; `docs/NOMENCLATURA.md` atua somente como fachada | não | CONFORME |
| `01_NUCLEO_COMUM.md` | linhas 183-185: schema atribuído ao antigo monólito, autoridade migrada | "antigo" e "autoridade migrada" | módulos proprietários | não | CONFORME |
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | linha 51: termo proprietário do papel atual da fachada | não histórico; declaração atual | fachada de compatibilidade e navegação | não | CONFORME |
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | linha 72: monólito antigo responsável por schema e semântica | "antigo monólito", "substituído pela fachada" | "Atualmente ... atua somente como fachada"; autoridade vigente nos módulos proprietários | não | CONFORME |
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | linha 116: schema e semântica nos módulos proprietários | não histórico; declaração atual | `docs/NOMENCLATURA.md` atua somente como fachada | não | CONFORME |

Critérios avaliados:

| Critério | Resultado |
| -------- | --------- |
| Estado `VIGENTE` preservado | CONFORME |
| Módulo continua como autoridade de seu domínio | CONFORME |
| `fachada_de_navegacao: docs/NOMENCLATURA.md` permanece correto | CONFORME |
| Referências ao papel anterior do monólito possuem marcador histórico explícito | CONFORME |
| Papel atual de fachada explicitado | CONFORME |
| Nenhuma frase apresenta a fachada como proprietária atual de schema, semântica, artefato ou definição | CONFORME |
| Proveniência histórica preservada | CONFORME |
| Nenhuma definição removida, transferida ou duplicada pelo patch | CONFORME |
| Nenhuma propriedade terminológica mudou indevidamente | CONFORME |

Resultado do achado: `RESOLVIDO`.

## 8. Auditoria de QA-F2-003

Achado original: a linha da ADR-0029 em `docs/adr/INDICE_ADR.md` não informava inequivocamente que a fase 2 aguardava QA.

Confirmação da linha atual:

| Critério | Resultado |
| -------- | --------- |
| ADR-0029 aceita e aplicada | CONFORME |
| Fase 1 aprovada | CONFORME |
| Fase 2 executada | CONFORME |
| QA inicial da fase 2 rejeitado | CONFORME |
| Patch aplicado | CONFORME |
| QA pós-patch pendente | CONFORME |
| Contém `QA pós-FASE_2 inicial: APLICACAO_ADR_FASE_2_REJECTED` | CONFORME |
| Contém `PATCH_APLICACAO_ADR_FASE_2 aplicado` | CONFORME |
| Contém `aguardando QA_POS_PATCH_APLICACAO_ADR_FASE_2` | CONFORME |
| Fase 2 não declarada aprovada | CONFORME |
| Ciclo não declarado encerrado | CONFORME |
| Coerência com seção 22 do relatório de aplicação | CONFORME |

`git diff --unified=0 -- docs/adr/INDICE_ADR.md` mostra somente a adição física da linha ADR-0029 em relação ao HEAD `c90349c`. Não há alteração física de outras linhas do índice no diff acumulado.

Resultado do achado: `RESOLVIDO`.

## 9. Auditoria da seção 22

| Critério | Resultado |
| -------- | --------- |
| QA de origem correto | CONFORME |
| Três achados listados | CONFORME |
| Seis arquivos alterados listados | CONFORME |
| Resultados apresentados como declaração do autor, não aprovação | CONFORME |
| Relatório de QA inicial preservado | CONFORME |
| QA pós-patch ainda não executado antes desta etapa | CONFORME |
| Buscas mecânicas registradas | CONFORME |
| Estado Git registrado | CONFORME |
| Encerramento literal presente | CONFORME |

Encerramento confirmado na seção 22:

```yaml
status_literal: APLICACAO_ADR_FASE_2_CORRIGIDA_AGUARDANDO_QA_POS_PATCH
proxima_categoria: QA_POS_PATCH_APLICACAO_ADR_FASE_2
```

## 10. Verificação de regressões focais

| Regressão focal | Resultado |
| --------------- | --------- |
| Referência nova para arquivo inexistente | não detectada nos seis arquivos do patch |
| Contradição entre leitura seletiva e fachada | não detectada |
| Módulo `01` ou `02` deixando de ser autoridade do domínio | não detectada |
| Remoção de definição vigente | não detectada |
| Duplicação de definição | não detectada |
| Alteração indevida de outra linha do índice de ADRs | não detectada no diff físico acumulado |
| Instrução operacional incompatível com contratos e módulos | não detectada |
| Relatório de aplicação contradizendo os arquivos corrigidos | não detectada |

`docs/build_docs/to_do.md` permaneceu inalterado no diff Git; suas referências a `NOMENCLATURA.md` foram tratadas como histórico operacional fora do patch, conforme seção 22.3 do relatório de aplicação.

## 11. Verificações mecânicas e Git

Comandos executados a partir da raiz do repositório:

```text
git branch --show-current
git log -1 --oneline
git status --short
git diff --name-only
git diff --stat
git diff --check
git diff --cached --name-only
```

Resultados:

```yaml
branch: master
HEAD: c90349c feat: implementa apresentacoes multinivel com modos por tela
HEAD_esperado: c90349c
stage_vazio: true
commit_executado: false
git_diff_check: OK
git_diff_cached_name_only: vazio
```

Estado observado antes da criação deste relatório:

```yaml
git_status_short:
  arquivos_rastreados_modificados: 21
  arquivos_nao_rastreados_relacionados_adr_0029: 9
  novo_relatorio_pos_patch_presente_antes_desta_etapa: false
git_diff_name_only:
  inclui_somente_arquivos_rastreados: true
  arquivos_listados: 21
git_diff_stat:
  arquivos: 21
  insercoes: 323
  delecoes: 1931
```

Confirmações adicionais:

| Verificação | Resultado |
| ----------- | --------- |
| Relatório de QA inicial não foi modificado nesta etapa | CONFORME |
| Relatório de QA fase 1 não foi modificado nesta etapa | CONFORME |
| `docs/build_docs/to_do.md` permaneceu inalterado | CONFORME |
| Nenhum arquivo auditado foi corrigido por este QA | CONFORME |
| Stage vazio | CONFORME |
| Commit não executado | CONFORME |

Verificações do novo relatório após escrita ficam registradas como responsabilidade desta etapa. Foram executadas ao final: newline final, fences balanceadas, ausência de trailing whitespace e ausência de marcadores de conflito.

## 12. Achados pós-patch

| Achado original | Resultado pós-patch | Evidência | Novo achado necessário |
| --------------- | ------------------- | --------- | ---------------------- |
| `QA-F2-001` | RESOLVIDO | `instruction.md` linhas 15, 80, 112; `prompts.md` linha 83 | não |
| `QA-F2-002` | RESOLVIDO | `01_NUCLEO_COMUM.md` linhas 81-86 e 183-185; `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` linhas 51, 72 e 116 | não |
| `QA-F2-003` | RESOLVIDO | `INDICE_ADR.md` linha 59; seção 22.5.3 do relatório de aplicação | não |

Achados novos deste QA pós-patch:

| ID | Severidade | Achado | Evidência | Corretivo |
| -- | ---------- | ------ | --------- | --------- |
| OBS-QA-POS-F2-001 | OBSERVACAO | O diff Git físico não isola o intervalo do patch porque o working tree contém mudanças acumuladas da ADR-0029 e fases anteriores. | `git status --short`, `git diff --name-only`, seção 22 do relatório de aplicação | não |
| OBS-QA-POS-F2-002 | OBSERVACAO | `docs/build_docs/to_do.md` mantém referências históricas ao monólito e `status: em_andamento`, mas não foi alterado pelo patch e não contém a instrução operacional corrigida em `instruction.md`/`prompts.md`. | `git diff -- docs/build_docs/to_do.md` vazio; seção 22.3 do relatório de aplicação | não |

```yaml
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
bloqueios: 0
novos_achados_corretivos: 0
```

## 13. Status final

```yaml
achados_iniciais_resolvidos: 3
achados_iniciais_nao_resolvidos: 0
novos_achados_corretivos: 0
observacoes: 2
status_literal: APLICACAO_ADR_FASE_2_POS_PATCH_APPROVED_WITH_NOTES
status_normalizado: approved_with_notes
```

## 14. Próxima categoria

```yaml
proxima_categoria: PREPARAR_COMMIT
executada: false
```

## 15. Encerramento

```yaml
etapa_executada: QA_POS_PATCH_APLICACAO_ADR_FASE_2
fase: FASE_2_MIGRACAO_DEFINITIVA
adr: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md

QA_inicial:
  arquivo: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0029_FASE-2.md
  status_literal: APLICACAO_ADR_FASE_2_REJECTED
  preservado: true
  alterado: false

patch:
  relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md
  secao: 22
  status_literal_entrada: APLICACAO_ADR_FASE_2_CORRIGIDA_AGUARDANDO_QA_POS_PATCH
  arquivos_alterados_declarados: 6

achados_originais:
  QA-F2-001: RESOLVIDO
  QA-F2-002: RESOLVIDO
  QA-F2-003: RESOLVIDO
  resolvidos: 3
  nao_resolvidos: 0

regressoes:
  novos_achados_corretivos: 0
  arquivos_fora_do_escopo: 0

relatorios:
  QA_inicial_preservado: true
  QA_pos_patch_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0029_FASE-2.md
  relatorios_separados: true

achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
bloqueios: 0

stage_vazio: true
commit_executado: false

status_literal: APLICACAO_ADR_FASE_2_POS_PATCH_APPROVED_WITH_NOTES
status_normalizado: approved_with_notes
proxima_categoria: PREPARAR_COMMIT
```
