---
rastreabilidade:
  etapa: QA_POS_PATCH_IMPLEMENTACAO
  objeto: H-0046
  artefato_principal: tela/renderizador.py
  cadeia_raiz: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0046.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0046_P01.md
  achados_retestados:
    - QA-IMP-H0046-01
    - QA-IMP-H0046-02

resultado:
  achados_resolvidos:
    - QA-IMP-H0046-01
    - QA-IMP-H0046-02
  achados_pendentes:
    - id: QA-PP-IMP-H0046-P01-01
      requisito_violado: "Relatório P01 deve registrar evidência factual da demonstração executada."
      evidencia_focal: "RELATORIO_PATCH_IMPLEMENTACAO_H-0046_P01.md:37 registra geometria {'largura': 80, 'altura_interna': 34}; a prova equivalente com largura 80 e altura 42 retornou {'largura': 80, 'altura_interna': 13}, embora tenha produzido 42 linhas de largura 80."
      impacto: "A evidência documental da demonstração dimensional do patch é incorreta; a execução funcional permaneceu verde."
      correcao_necessaria: "Corrigir o valor de geometria registrado no relatório P01 e repetir a validação documental correspondente."
  achados_novos:
    - QA-PP-IMP-H0046-P01-01
  autoridades_unicas:
    status: PASS
    contexto: "Os três símbolos têm uma definição AST em contexto_execucao.py; matriz_participantes.py apenas os importa nominalmente."
    ansi: "Os seis símbolos têm uma definição AST em texto_ansi.py; barra_menus.py apenas os importa nominalmente."
    identidade_runtime: PASS
  testes_focais:
    tela/teste_renderizador.py: "371 passed"
    tela/teste_paginacao.py: "13 passed"
    tela/teste_navegacao.py: "41 passed"
    demo/teste_demo_paginacao.py: "128 passed"
    demo/teste_explorar_barra_de_menus.py: "19 passed"
  suite_completa:
    status: PASS
    resultado: "970 passed"
  demonstracao:
    status: PASS
    resultado: "demo/demo.py --help passou; a demonstração normativa em larguras 80 e 42, altura 40, passou com geometria_console coerente."
    desvio_registrado: "demo/teste_demo.py -k largura_explicita or altura_explicita retornou exit 5 com 56 deselected, conforme nota não bloqueante já registrada no IMP-0046."
  relatorios:
    IMP-0046: "PASS: HEAD_inicial correto; resíduos classificados como NAO_CONFIRMADO ou GERADO_DURANTE_QA sem atribuição indevida; exit 5 registrado."
    RELATORIO_PATCH_IMPLEMENTACAO_H-0046_P01: "PENDENTE: identifica os dois achados, os três arquivos alterados e as provas, mas contém o valor dimensional incorreto descrito acima."
  verificacoes_focais:
    - "PASS: fachada pública, origens e identidades das reexportações."
    - "PASS: fachada sem lógica, importação isolada, ciclo AST e ausência de importação inversa."
    - "PASS: nenhum consumidor externo migrado; propriedade AST e aliases técnicos nominais confirmados."
    - "PASS: identidade de _navegacao_atual e ciclo de acesso/reset do quadro mínimo."
    - "LIMITAÇÃO DE PROVENIÊNCIA: git diff focal veio vazio porque matriz_participantes.py e barra_menus.py são não rastreados; o delta P01 foi confirmado apenas pelo manifesto, estado Git e relatório P01."
  status: IMPLEMENTATION_PATCH_REQUIRED
  bloqueios: []
---
