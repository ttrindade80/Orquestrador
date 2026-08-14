---
name: RELATORIO_QA_HANDOFF_H-0063_P01
description: Auditoria independente do handoff H-0063 após o patch P01
metadata:
  type: relatorio_qa
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  status: H1_HANDOFF_APPROVED
  data: 2026-08-12
rastreabilidade:
  autorizacao_qa: QA_HANDOFF H-0063 pós-P01
  handoff_origem: docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  relatorio_qa_anterior: docs/relatorios/RELATORIO_QA_HANDOFF_H-0063.md
  contrato_alvo:
    - docs/contratos/contrato_console.md §§22.11, 22.16–22.18
    - docs/contratos/contrato_barra_de_menus.md §§8.2, 8.2.1 e 9
  cadeia_raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0063.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0063_P01.md
  achados_tratados:
    - H0063-QA-001
    - H0063-QA-002
---

# RELATORIO_QA_HANDOFF_H-0063_P01 — QA pós-patch

## 1. Identificação e status

```yaml
revisao: H-0063 — reteste documental pós-P01
etapa_qa: QA_HANDOFF
camada_auditada: HANDOFF
status_literal: H1_HANDOFF_APPROVED
status_normalizado: HANDOFF_APPROVED
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
autoridades_materiais:
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0063_P01.md
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0063.md
  - docs/handoff/H-0055-dois-niveis-por-foco.md
  - config/telas/demo/h0055_dois_niveis_por_foco.json
escopo:
  - reteste exclusivo de H0063-QA-001 e H0063-QA-002
  - coerência do handoff corrigido e suficiência da evidência do P01
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: H0063-QA-001
    comando_ou_metodo: leitura focal das §§4.4, 5, 6.2, 13 e 16 do H-0063; comparação com contrato_console §§22.11 e 22.16–22.18 e H-0055
    evidencia_focal: >-
      O handoff distingue pai/filho corrente de filho escolhido, determina
      escolha exclusiva por pai, transferência somente por Espaço no filho,
      preservação por Esc, e separa esse estado de qualquer mutação de estilo.
      Também declara literalmente dois_niveis_por_foco e
      politica_selecao: multipla como compatibilidade vigente.
    resultado: OK
  - id: H0063-QA-002
    comando_ou_metodo: leitura focal da §6.3 do H-0063; comparação com contrato_barra_de_menus §9 e fixture H-0055
    evidencia_focal: >-
      O rótulo inventado foi removido: a barra usa [␣] Selecionar, cobre
      entrada nos filhos e transferência de escolha sem chip concorrente,
      explicita Esc contextual nos dois níveis e mantém [?] Ajuda obrigatório,
      ativo e último. A expressão entrada no nível permanece apenas em
      negações/explicações, não como identidade de chip.
    resultado: OK
  - id: evidencia_do_patch
    comando_ou_metodo: leitura do relatório autorizado P01 e inspeção do estado Git focal
    evidencia_focal: >-
      O relatório P01 identifica os dois achados, descreve o delta material e
      registra as verificações lexicais executadas. O handoff e o relatório P01
      estão não rastreados; por isso não existe baseline em HEAD/index para
      reconstruir o diff original, limitação já registrada no P01.
    resultado: OK
```

## 4. Achados

`nenhum`.

## 5. Reteste pós-P01

```yaml
raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0063.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0063_P01.md
achados_resolvidos:
  - H0063-QA-001
  - H0063-QA-002
achados_pendentes: []
novos_achados: []
```

## 6. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
  staged: []
  unstaged: alterações paralelas pré-existentes fora do escopo nominal deste QA
  nao_rastreados:
    - docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0063_P01.md
    - docs/relatorios/RELATORIO_QA_HANDOFF_H-0063_P01.md
itens_inesperados:
  - item: alterações paralelas no worktree
    origem: NAO_CONFIRMADA
    evidencia: preservadas e não atribuídas ao handoff ou ao P01; não interferem na leitura focal
```

## 7. Conclusão

H0063-QA-001 e H0063-QA-002 estão resolvidos no conteúdo atual do H-0063 e a
evidência factual do P01 é suficiente para o reteste documental. Não há
achado novo ou pendência dentro do escopo deste QA. O status aplicável é
`H1_HANDOFF_APPROVED`.
