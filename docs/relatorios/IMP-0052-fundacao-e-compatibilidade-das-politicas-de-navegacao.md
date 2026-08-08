handoff: H-0052
status_implementacao: IMPLEMENTED
arquivos_alterados:
  - tela/navegacao.py
  - tela/carregamento/envelope_pre_adr_0028.py
  - tela/teste_navegacao.py
  - tela/teste_loader.py
arquivos_criados:
  - config/telas/demo/h0052_nivel_unico_explicito.json
  - config/telas/demo/h0052_tabela_passiva.json
  - docs/relatorios/IMP-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
testes_focais:
  comando: >-
    PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py
    tela/teste_loader.py tela/teste_paginacao.py -v
  resultado: 147 passed, 0 failed
suite_integral:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  resultado: 1059 passed, 0 failed, 30.27s
demonstracao:
  comportamento: >-
    Legado e nivel_unico explicito preservam foco, cursor e quatro setas;
    tabela e passiva, sem foco, cursor ou [✥]. Os cinco literais sao
    transportados, e os tres modos futuros permanecem inertes.
  fixtures_validadas: >-
    h0052_nivel_unico_explicito.json e h0052_tabela_passiva.json foram
    carregadas pelos testes do loader; h0045_validacao_nova_pagina.json foi
    preservada como caso legado.
  comandos_manuais:
    - >-
      PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela
      config/telas/demo/h0045_validacao_nova_pagina.json
    - >-
      PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela
      config/telas/demo/h0052_nivel_unico_explicito.json
    - >-
      PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela
      config/telas/demo/h0052_tabela_passiva.json
validacao_manual: NAO_REALIZADA_PELO_AGENTE; pendente de observacao TTY pelo usuario
desvios: nenhum
excecoes: nenhuma
bloqueios: nenhum
