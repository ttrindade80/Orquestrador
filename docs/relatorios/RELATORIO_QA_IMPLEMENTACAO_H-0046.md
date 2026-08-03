---
rastreabilidade:
  etapa: QA_IMPLEMENTACAO
  objeto: H-0046
  artefato_principal: tela/renderizador.py
  handoff: docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md
  implementacao: docs/relatorios/IMP-0046-modularizacao-estrutural-do-renderizador.md

resultado:
  arquivos_auditados:
    - handoff H-0046 e relatório IMP-0046
    - tela/renderizador.py e baseline Git 26a43654b13f6ccf28a59208aa08e819ebe80170
    - tela/renderizacao/*.py (15 módulos)
    - diff focal de tela/teste_renderizador.py
  verificacoes_estruturais:
    - "Git: master, HEAD 26a43654b13f6ccf28a59208aa08e819ebe80170; nenhum código, teste ou configuração fora do manifesto foi confirmado. Documentos e tela/__pycache__ já constavam do estado inicial, com proveniência NAO_CONFIRMADO; tela/renderizacao/__pycache__ foi gerado pelas provas de importação desta auditoria."
    - "AST: 38 símbolos públicos preservados; negativos históricos preservados; corpos equivalentes salvo os acessores de estado e referências internas autorizadas."
    - "Fachada: 57 linhas, sem FunctionDef/AsyncFunctionDef/Lambda/ClassDef, imports nominais fechados, sem chamadas/cálculos de módulo e identidades corretas."
    - "Passaram importações isoladas, mapa físico nominal, aliases técnicos, detector sintético/real de ciclos, importação inversa e busca de consumidores externos."
    - "Estado: identidade de _navegacao_atual, proprietário único do bool, ativação/consulta/reset e reinício de renderizar_tela confirmados por inspeção e execução."
    - "FALHA estrutural: há proprietários duplicados para DESCONTO_ESTRUTURAL_CONSOLE e helpers de contexto em contexto_execucao.py/matriz_participantes.py; primitivas ANSI também são redefinidas em barra_menus.py apesar da autoridade em texto_ansi.py."
  testes_focais:
    - "paginacao 13; navegacao 41; renderizador 371; resultado_execucao 56"
    - "demo 56; console 6; console_modos 11; navegacao 19; paginacao 128"
    - "selecao 10; diagnostico 6; explorar_barra_de_menus 19 — todos passed"
  suite_completa: "exit 0; 970 passed; nenhum skip/xfail relacionado"
  demonstracao: "demo/demo.py --help exit 0; demonstração dimensional normativa 80/42 passou e comprovou saída/geometria coerentes"
  desvio_exit_5: "demo/teste_demo.py -k 'largura_explicita or altura_explicita' exit 5, 56 deselected; o filtro não seleciona testes coletáveis e a demonstração dimensional cobre diretamente a propriedade. Nota não bloqueante."
  achados:
    - id: QA-IMP-H0046-01
      requisito_violado: "H-0046 seção 3.2, autoridades únicas; D-MOD-08 itens 7 e 10"
      evidencia_focal: "AST e inspeção: DESCONTO_ESTRUTURAL_CONSOLE em contexto_execucao.py:216 e matriz_participantes.py:145; _item_corrente_de_contexto e _itens_navegaveis_do_elemento materializados nos dois módulos; _ANSI_POR_NOME_SEMANTICO, _ANSI_RESET_FG, _codigo_ansi_de_cor, _largura_sem_ansi, _cortar_sem_ansi e _ljust_sem_ansi materializados em barra_menus.py:118-200 e texto_ansi.py:5-87."
      impacto: "As responsabilidades não têm propriedade nominal única. A fachada reexporta contexto/texto_ansi, mas consumidores internos resolvem cópias locais; a prova nominal vigente não detecta duplicidade."
      correcao_necessaria: "Remover as materializações duplicadas e fazer todos os consumidores referenciarem as autoridades de contexto_execucao.py e texto_ansi.py; repetir as provas estruturais e a suíte."
    - id: QA-IMP-H0046-02
      requisito_violado: "H-0046 seção 9; rastreabilidade correta do estado Git e resíduos"
      evidencia_focal: "IMP-0046:72 declara documentos/bytecodes presentes no baseline e NAO_CONFIRMADO: nenhum. O estado Git inicial já mostrava os documentos e tela/__pycache__, mas git cat-file -e contra o HEAD inicial confirmou que não estavam no baseline; tela/renderizacao/__pycache__ surgiu durante as provas desta auditoria."
      impacto: "A proveniência do worktree está documentada incorretamente e o relatório IMP não classifica os resíduos com a cautela exigida."
      correcao_necessaria: "Corrigir IMP-0046 para registrar os caminhos extra-manifesto como NAO_CONFIRMADO, sem atribuí-los ao implementador, e atualizar a descrição do delta observado."
  status: IMPLEMENTATION_PATCH_REQUIRED
  bloqueios: []
---

## Síntese

A API, o comportamento observado, os testes, a fachada, os ciclos e a
importação pública foram aprovados. O patch não pode ser fechado porque a
arquitetura física não preserva as autoridades únicas exigidas e o relatório
de implementação registra uma proveniência Git não demonstrada.

Não foram aplicados patches, alterados testes, feitos stage ou commit nesta
auditoria.
