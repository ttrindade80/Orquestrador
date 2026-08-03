---
rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0047
  artefato_principal: docs/handoff/H-0047-modularizacao-estrutural-do-loader.md
  autoridade_principal: docs/adr/ADR-0039-modularizacao-estrutural-do-runtime-de-telas.md

execucao:
  status: H2_HANDOFF_PATCH_REQUIRED
  arquivos_criados:
    - docs/relatorios/RELATORIO_QA_HANDOFF_H-0047.md

resultado:
  verificacoes_executadas:
    - estado Git transportado: branch master, HEAD esperado e stage vazio
    - leitura integral do manifesto fechado e dos oito arquivos autorizados
    - AST de tela/loader.py e fronteira de imports com tela/modelo.py
    - consumidores reais e conjunto efetivo de 24 símbolos reexportados
    - buscas de whitebox/monkeypatch, constante não consumida e caminhos nominais
    - fixture nominal e demonstração não interativa, sem escrita persistente
  achados:
    - id: H0047-QA-001
      requisito_violado: D-MOD-08 item 8; seção 7, prova 2 — o detector de ciclos deve validar o grafo real de módulos.
      evidencia_focal: "O DFS percorre grafo.get(d, ()) sem exigir que d exista em grafo; uma dependência para módulo inexistente é tratada como folha e pode produzir OK."
      impacto: Uma implementação pode conter import interno digitado incorretamente ou apontar para módulo ausente sem que a prova estrutural acuse falha.
      correcao_necessaria: Exigir que toda dependência interna esteja entre os arquivos do pacote antes do DFS e emitir falha com a aresta e o módulo ausente.
      camada_responsavel: Handoff, seção 7.2.
    - id: H0047-QA-002
      requisito_violado: D-MOD-08 itens 7 e 10; seção 7, prova 7 — proprietário nominal único e localização direta.
      evidencia_focal: "materializado_no_proprietario verifica apenas presença AST no arquivo indicado e hasattr; esperados cobre amostras, não todos os símbolos declarados, e não há índice de definições duplicadas entre módulos."
      impacto: A prova pode aprovar proprietário duplicado ou deixar funções/constantes extraídas no módulo errado, criando falsa segurança sobre a arquitetura nominal.
      correcao_necessaria: Indexar todas as definições de nível superior dos módulos previstos, comparar com o mapa integral da seção 4.2 e exigir exatamente um proprietário por símbolo; manter a checagem de identidade da fachada.
      camada_responsavel: Handoff, seção 7.7 e mapeamento da seção 4.2.
    - id: H0047-QA-003
      requisito_violado: D-MOD-08 item 9; seções 5.3 e 7, prova 3 — nenhum módulo interno pode importar a fachada.
      evidencia_focal: "A prova usa apenas regex para 'from tela.loader' e 'import tela.loader'; não cobre, por exemplo, 'from tela import loader', importação de tela seguida de tela.loader ou carregamento dinâmico por importlib/__import__."
      impacto: Uma dependência inversa pode escapar da prova e quebrar a direção declarada ou introduzir ciclo em forma não capturada.
      correcao_necessaria: Substituir a busca por análise AST das formas estáticas de importação, incluindo a forma via pacote, e declarar/verificar explicitamente a política para carregamento dinâmico.
      camada_responsavel: Handoff, seções 5.3 e 7.3.
    - id: H0047-QA-004
      requisito_violado: D-MOD-03, D-MOD-04 e D-MOD-08 item 10 — todas as dependências necessárias e proprietários devem estar nominalmente fechados.
      evidencia_focal: "No código atual, TelaIdIncorreto (tela/loader.py:112-122) usa default esperado=_ID_TELA_RAIZ; a arquitetura move a classe para erros.py sem dependências e move _ID_TELA_RAIZ para tela_json.py, mas não declara essa relação nem uma preservação verificável do default."
      impacto: A extração direta pode falhar no import ou alterar a assinatura/valor default da exceção; uma duplicação literal não documentada também enfraquece a propriedade nominal.
      correcao_necessaria: Fechar no handoff o proprietário de _ID_TELA_RAIZ e a aresta correspondente, ou especificar a preservação do default por literal e adicionar prova de assinatura e valor.
      camada_responsavel: Handoff, seção 4.2–4.3 e prova de fachada.
  bloqueios: []
