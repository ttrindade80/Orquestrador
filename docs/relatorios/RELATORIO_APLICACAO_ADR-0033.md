---
name: REL-ALT-0033-aplicacao-adr-0033
description: Resultado factual da aplicação da ADR-0033 (separação entre backlog, histórico e arquivo documental)
metadata:
  type: relatorio_aplicacao_alteracao
  tipo_execucao: APLICAR_ADR
  status: ADR_APPLICATION_COMPLETED
  data: 2026-07-27
rastreabilidade:
  etapa: APLICAR_ADR
  objeto: docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
  artefato_principal: docs/backlog.md
  autoridade_principal: docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
  cadeia_raiz: docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0033.md
  achados_tratados: []
---

# REL-ALT-0033 — Aplicação da ADR-0033

## 1. Identificação e status

```yaml
tipo_execucao: APLICAR_ADR
objeto: docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
status_literal: ADR_APPLICATION_COMPLETED
```

## 2. Delta material

```yaml
delta_material:
  - docs/backlog.md passa a conter somente ITEM-0003 a ITEM-0017, nos estados planejado/bloqueado/em_andamento/pronto_para_handoff
  - ITEM-0002 removido do backlog e registrado como CONCLUIDO em docs/HISTORICO.md
  - docs/HISTORICO.md criado com as quatro seções (Concluídos, Cancelados, Substituídos, Incompatíveis)
  - 32 itens concluido de to_do.md, mais DOC-0019 e DOC-0022, registrados como CONCLUIDO (total 34, mais ITEM-0002 = 35 entradas em Concluídos)
  - DOC-B003, DOC-B004, DOC-B007, DOC-B008, DOC-B009 registrados como CANCELADO
  - ITEM-0015, ITEM-0016, ITEM-0017 criados no backlog, todos bloqueado
  - docs/arquivo/README.md criado com as declarações de governança do arquivo
  - docs/build_docs/instruction.md, prompts.md e to_do.md movidos por git mv para docs/arquivo/build_docs/, cada um recebendo o aviso de documento histórico
  - docs/build_docs/ deixou de existir (diretório vazio removido após a migração)
  - docs/INDICE.md atualizado distinguindo backlog, histórico e arquivo
  - docs/adr/INDICE_ADR.md atualizado com a linha da ADR-0033
delta_nomenclatura:
  modulos_alterados: []
  termos_criados: []
  termos_alterados: []
  aliases_ou_historicos: []
```

## 3. Arquivos

```yaml
arquivos_criados:
  - caminho: docs/HISTORICO.md
    finalidade: registro compacto de itens encerrados
  - caminho: docs/arquivo/README.md
    finalidade: governança da área de documentos históricos
  - caminho: docs/relatorios/RELATORIO_APLICACAO_ADR-0033.md
    finalidade: este relatório
arquivos_alterados:
  - caminho: docs/backlog.md
    delta: regra inicial reescrita para trabalho ativo; exemplos ITEM-0000/ITEM-0001 removidos; ITEM-0002 removido; ITEM-0004 ajustado; ITEM-0015 a ITEM-0017 adicionados
  - caminho: docs/INDICE.md
    delta: estrutura esperada e tabela de artefatos passam a distinguir backlog, histórico e arquivo
  - caminho: docs/adr/INDICE_ADR.md
    delta: linha da ADR-0033 adicionada
arquivos_removidos:
  - caminho: docs/build_docs/instruction.md
    motivo_autorizado: migração via git mv para docs/arquivo/build_docs/instruction.md (D-HIST-08)
  - caminho: docs/build_docs/prompts.md
    motivo_autorizado: migração via git mv para docs/arquivo/build_docs/prompts.md (D-HIST-08)
  - caminho: docs/build_docs/to_do.md
    motivo_autorizado: migração via git mv para docs/arquivo/build_docs/to_do.md (D-HIST-08)
```

## 4. Verificações

```yaml
verificacoes_executadas:
  - comando_ou_metodo: grep de ITEM-0002 e ITEM-0003 a ITEM-0017 em docs/backlog.md
    resultado_compacto: ITEM-0002 ausente; ITEM-0003 a ITEM-0017 presentes uma única vez cada
    prova_semantica: backlog contém somente os itens autorizados
  - comando_ou_metodo: grep de Status em docs/backlog.md
    resultado_compacto: somente bloqueado e planejado como estados de item real (linha de Formato preservada como template)
    prova_semantica: nenhum estado de encerramento presente
  - comando_ou_metodo: grep de DOC-B009 no bloco de ITEM-0004
    resultado_compacto: 0 ocorrências
    prova_semantica: dependência nominal removida conforme instrução
  - comando_ou_metodo: grep de "Origem legada" em docs/backlog.md
    resultado_compacto: 0 ocorrências
    prova_semantica: campo proibido ausente
  - comando_ou_metodo: varredura de identificadores duplicados entre seções de docs/HISTORICO.md
    resultado_compacto: nenhum identificador duplicado
    prova_semantica: cada item aparece em uma única seção
  - comando_ou_metodo: test -e / test -f nos seis caminhos de docs/build_docs/ e docs/arquivo/build_docs/
    resultado_compacto: três ausentes na origem, três presentes no destino
    prova_semantica: movimentação Git confirmada
  - comando_ou_metodo: "diff -u <(git show HEAD:<arquivo>) <(sed '1,7d' <arquivo migrado>) para os três arquivos"
    resultado_compacto: saída vazia nos três casos
    prova_semantica: somente o aviso de sete linhas (seis de aviso + linha em branco) foi acrescentado; conteúdo histórico preservado integralmente
  - comando_ou_metodo: git diff --check
    resultado_compacto: sem saída (sem espaço em branco problemático)
    prova_semantica: integridade textual das alterações
  - comando_ou_metodo: git status --short --untracked-files=all
    resultado_compacto: somente arquivos autorizados (criados, alterados, renomeados) e relatórios não rastreados já esperados da sessão anterior
    prova_semantica: nenhuma alteração fora do escopo autorizado
```

## 5. Achados, bloqueios e ressalvas

```yaml
achados: []
bloqueios: []
ressalvas:
  - "O diretório docs/build_docs/ ficou vazio após os três git mv e foi removido do sistema de arquivos (diretório vazio não é rastreado pelo Git; remoção não afeta histórico nem staging)."
```
