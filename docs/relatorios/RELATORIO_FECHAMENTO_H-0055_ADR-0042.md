# Relatório de fechamento — H-0055 / ADR-0042

```yaml
rastreabilidade:
  etapa: FECHAMENTO
  ADR: ADR-0042
  handoff: H-0055
  capacidade: dois_niveis_por_foco

estado_final:
  qa_handoff: H1_HANDOFF_APPROVED
  qa_implementacao: I5_MANUAL_VALIDATION_REQUIRED
  validacao_manual: MANUAL_VALIDATION_APPROVED
  achados_pendentes: []

verificacoes:
  git_diff_check: CONFORME
  git_diff_cached_check: CONFORME
  manifesto_stage: CONFORME
  stage_nominal: STAGE_PRONTO_PARA_COMMIT
```

## Reconciliação

- O handoff e os relatórios de QA/manual preservam os dois níveis por foco,
  `[Esc] Sair` nos pais, `[Esc] Voltar` nos filhos, D23 fixo em
  `somente_nao_verboso`, ausência de `modo_inicial` e `V`, e as fronteiras
  negativas de H-0055.
- `docs/backlog.md` foi reconciliado somente no delta de H-0055: a capacidade
  passou a constar como concluída após implementação, QA e validação manual.
  Os deferimentos, o ITEM-0025 e o ITEM-0026 foram preservados.
- Todos os relatórios históricos do manifesto estão presentes e foram
  preservados; nenhum relatório P01/P02/P03 foi reescrito ou removido.

## Resíduos e normalização

Nenhum resíduo material de H-0055 foi identificado. Nada foi removido. Não
houve correção semântica de código; a reconciliação foi documental e o
whitespace/EOF do conjunto do manifesto ficou conforme. Não foi necessária
nova rodada de testes.

## Artefatos e stage

Todos os artefatos obrigatórios foram materializados. A comparação nominal do
stage foi feita por caminho, sem arquivo estranho e sem item esperado ausente:

```text
demo/demo.py
demo/teste_demo_console.py
docs/backlog.md
tela/carregamento/envelope_pre_adr_0028.py
tela/navegacao.py
tela/renderizacao/console.py
tela/selecao.py
tela/teste_navegacao.py
config/telas/demo/h0055_dois_niveis_por_foco.json
config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json
docs/handoff/H-0055-dois-niveis-por-foco.md
docs/relatorios/IMP-0055-dois-niveis-por-foco.md
docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0055.md
docs/relatorios/RELATORIO_QA_HANDOFF_H-0055.md
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0055_P01.md
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0055_P02.md
docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0055_P02.md
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0055_P03.md
docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0055_P03.md
docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0055.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0055_P01.md
docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0055_P01.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0055_P02.md
docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0055_P02.md
docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0055.md
docs/relatorios/RELATORIO_FECHAMENTO_H-0055_ADR-0042.md
```

`git diff --check` e `git diff --cached --check` devem permanecer sem saída.

Mensagem de commit proposta, não executada:

```text
feat: implementa dois niveis por foco no console
```

Nenhum commit ou push foi executado. Próxima ação: `COMMIT_MANUAL`.
