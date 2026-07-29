---
name: REL-QA-H0041-HANDOFF-P02
description: "QA independente do patch documental P02 do handoff H-0041"
metadata:
  type: handoff_qa
  status: H2_HANDOFF_PATCH_REQUIRED
  id: QA-H0041-HANDOFF-P02
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  data_criacao: 2026-07-28
rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0041
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_H-0041_HANDOFF_P02.md
  patch_auditado: P02
  achados_retestados:
    - H0041-MANUAL-R02-001
    - H0041-MANUAL-R02-002
    - H0041-MANUAL-R02-003
---

# QA H-0041 — Handoff P02

## 1. Etapa única

`QA_HANDOFF` do delta documental P02. Não houve correção, implementação P04, validação TTY nem operação Git de escrita.

## 2. Evidência focal

O gate Git correspondeu ao estado transportado: `master`, HEAD `721f8f1`, stage vazio, `git diff --check` limpo; handoff e relatório P02 presentes, e este relatório QA ausente antes desta execução. O `git diff --` do handoff não retornou delta no worktree.

O handoff incorpora a R02, mantém explicitamente pendentes `H0041-MANUAL-R02-001`, `-002` e `-003`, e fixa `cor_inativo: cinza` em `config/estilo.json`. Para P04, a lista nominal, sem curingas, autoriza somente configuração, loader, renderer, dispatch em `demo/demo.py`, fixture, quatro testes e o relatório P04; todos os caminhos técnicos listados existem e o relatório P04 não existe.

A cadeia vigente confirma a base factual: `EstiloResolvido` e `carregar_estilo` ainda não transportam `cor_inativo`; `_texto_chip_barra` ainda usa `texto.lower()` quando inativo. O P04 autoriza precisamente a substituição por estilo resolvido, sem literal ANSI/cinza no renderer, e preserva consoles sem seleção múltipla. O handoff exige `Marcar`, `Todos` e `Executar` com capitalização normal, cinza somente para chips inativos, nenhum efeito ao acioná-los e restauração da cor após o chip.

O caminho obrigatório `tecla → dispatch → selecionar todos → atualizar estado → redesenhar` está documentado para o ponto de entrada/loop TTY, não apenas chamada direta. Exige os quatro IDs, quatro `tg` e `Executar` cinza no mesmo quadro; os testes nominais comportam estilo, chips, Enter/Todos, regressões, Esc, reconciliação e associação participante→ID. A revalidação futura permanece corretamente ordenada: P04, QA pós-patch e TTY pelo usuário.

## 3. Achado material

### H0041-HANDOFF-P02-DOC-001

- Requisito: o relatório P02 deve registrar fatos materiais e os arquivos criados pela própria execução.
- Evidência: a seção 3 declara `arquivos_criados: []`; a seção 5 declara simultaneamente que “único arquivo criado é este relatório”. A verificação de QA do template inclui a suficiência factual dos artefatos criados/alterados.
- Impacto: a rastreabilidade do patch é internamente contraditória e não é factual quanto ao artefato P02 criado.
- Correção necessária: incluir `docs/relatorios/RELATORIO_PATCH_H-0041_HANDOFF_P02.md` em `arquivos_criados`.

## 4. Status

```yaml
status_literal: H2_HANDOFF_PATCH_REQUIRED
achados_pendentes:
  - H0041-MANUAL-R02-001
  - H0041-MANUAL-R02-002
  - H0041-MANUAL-R02-003
novos_achados:
  - H0041-HANDOFF-P02-DOC-001
proxima_acao: corrigir somente a exatidao factual do RELATORIO_PATCH_H-0041_HANDOFF_P02.md e submeter novo QA_HANDOFF
```
