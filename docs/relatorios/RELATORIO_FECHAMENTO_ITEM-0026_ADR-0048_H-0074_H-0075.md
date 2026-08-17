status: STAGE_PRONTO_PARA_COMMIT
branch: master
HEAD: 3a8425a0c198dc3bcd43a1392e210993332eab53
item: ITEM-0026
adr: ADR-0048
handoffs:
  - H-0074
  - H-0075

validacoes_finais:
  qa_h0074: I1_IMPLEMENTATION_APPROVED
  manual_h0074: MANUAL_VALIDATION_APPROVED
  qa_h0075: QA pós-patch aprovado; QA-IMPL-H0075-001 resolvido; novos_achados: nenhum
  manual_h0075: MANUAL_VALIDATION_APPROVED pelo usuário, em cópia temporária
  testes_focais: >-
    Na árvore real, sem hook, coleta bloqueada por SyntaxError histórico em
    tela/carregamento/tela_json.py:528. Em cópia temporária normalizada, sem
    hook, 41 passed e 165 deselected; os testes usam tmp_path/cópias para
    persistência.
  suite_canonica: >-
    118 coletados / 44 errors during collection na árvore real;
    PREEXISTENTE_NAO_CAUSAL, por resíduos EOF em tela/carregamento/tela_json.py,
    tela/estilo.py, tela/renderizacao/texto_ansi.py e testes históricos fora
    do manifesto.
  diff_check: PASS nos arquivos nominais; ver auditoria do stage abaixo

reconciliacao_documental:
  backlog: >-
    ITEM-0026 removido do backlog ao ser encerrado, conforme a convenção
    vigente; encerramento registrado em docs/HISTORICO.md.
  indices: >-
    docs/adr/INDICE_ADR.md atualizado para aplicação pós-P02 aprovada,
    H-0074/H-0075 concluídos e ITEM-0026 encerrado.
  contratos: >-
    contrato_console.md §26 e contrato_json_console.md §16/§16.7 refletem
    documento externo → pai → filho_default, baseline/candidato, Aplicar por
    divergência, confirmação genérica, ABORTADO, CONFIRMADO e fail-closed.
  nomenclatura: >-
    Módulos 32, 42 e 43 reconciliados com a autoridade final e sem fallback
    para o primeiro filho.
  adr: >-
    ADR-0048 em ADR_APPLIED, com D-0026-12/filho_default materializado e
    critérios de aplicação marcados como atendidos.
  handoffs: >-
    H-0074 e H-0075 em CONCLUIDO, com QA pós-patch, QA técnico e validação
    manual aprovados.

higiene_mecanica:
  arquivos_normalizados:
    - demo/demo.py
    - docs/HISTORICO.md
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
    - docs/relatorios/RELATORIO_QA_HANDOFF_H-0075.md
  residuos_historicos_fora_escopo:
    - tela/carregamento/tela_json.py:528
    - tela/estilo.py:540
    - tela/renderizacao/texto_ansi.py:213
    - testes e JSONs históricos com resíduos equivalentes

classificacao_manifesto:
  ITEM0026_NOMINAL: 52 caminhos, listados abaixo
  PREEXISTENTE_NAO_CAUSAL:
    - resíduos históricos fora do manifesto, não staged
  OUTRA_ATIVIDADE: []
  DUVIDOSO: []

manifesto_nominal:
  - config/telas/demo/h0055_dois_niveis_por_foco.json
  - config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json
  - config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json
  - config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json
  - demo/demo.py
  - demo/teste_demo_filho_default_h0075.py
  - docs/HISTORICO.md
  - docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md
  - docs/adr/INDICE_ADR.md
  - docs/backlog.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/handoff/H-0074-filho-default-carregamento-baseline-runtime.md
  - docs/handoff/H-0075-aplicar-confirmar-persistir-filho-default.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
  - docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0048.md
  - docs/relatorios/RELATORIO_CRIACAO_ADR-0048.md
  - docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0074.md
  - docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0075.md
  - docs/relatorios/RELATORIO_FECHAMENTO_ITEM-0026_ADR-0048_H-0074_H-0075.md
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0074.md
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0075.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_ITEM-0023_ITEM-0024_ITEM-0026_R01.md
  - docs/relatorios/RELATORIO_PATCH_ADR-0048_P01.md
  - docs/relatorios/RELATORIO_PATCH_ADR-0048_P02.md
  - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0048_P01.md
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0074_P01.md
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0075_P01.md
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0075_P02.md
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0075_P01.md
  - docs/relatorios/RELATORIO_QA_ADR-0048.md
  - docs/relatorios/RELATORIO_QA_ADR-0048_POS_P01.md
  - docs/relatorios/RELATORIO_QA_ADR-0048_POS_P02.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0048.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0048_POS_P01.md
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0074.md
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0074_POS_P01.md
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0075.md
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0075_POS_P01.md
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0075_POS_P02.md
  - docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0074.md
  - docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0075.md
  - docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0075_POS_P01.md
  - tela/carregamento/conteudo_externo.py
  - tela/modelo.py
  - tela/navegacao.py
  - tela/selecao.py
  - tela/teste_filho_default_h0075.py
  - tela/teste_loader.py
  - tela/teste_navegacao.py

stage:
  arquivos: manifesto_nominal acima
  diff_cached_check: PASS

bloqueios: []
