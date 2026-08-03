# Relatório QA pós-patch do H-0046 — P01

```yaml
rastreabilidade:
  etapa: QA_POS_PATCH_HANDOFF
  objeto: H-0046
  artefato_principal: docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md
  cadeia_raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0046.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0046_P01.md
  achados_retestados:
    - QA-H0046-01
    - QA-H0046-02
    - QA-H0046-03
    - QA-H0046-04
    - QA-H0046-05
    - QA-H0046-06

resultado:
  achados_resolvidos:
    - QA-H0046-01
    - QA-H0046-03
    - lacuna_reset_quadro_minimo_lancador_ativo
  achados_pendentes:
    - id: QA-H0046-02
      requisito_violado: "§3.2–§3.3 — dependências declaradas e direção acíclica"
      evidencia_focal: "Persistem dependências reais não declaradas: _linha_conteudo usa _cortar_sem_ansi e _ljust_sem_ansi da barra; a matriz usa _participantes_de_conteudo_externo; paginacao_interna importa localmente tela.navegacao."
      impacto: "A implementação ainda precisa inventar ou relocar dependências para concluir a arquitetura."
      correcao_necessaria: "Registrar nominalmente todas essas dependências e ajustar o grafo acíclico."
    - id: QA-H0046-04
      requisito_violado: "§7.2 e D-MOD-08 item 8 — prova de ciclos"
      evidencia_focal: "O detector cobre imports relativos, ast.Import, ast.ImportFrom específicos e travessia transitiva, mas não normaliza from tela.renderizacao import modulo; essa forma pode ocultar uma aresta de ciclo."
      impacto: "Um ciclo usando essa sintaxe absoluta pode ser aprovado pela prova."
      correcao_necessaria: "Normalizar essa forma para o submódulo ou proibi-la explicitamente e fazê-la falhar."
    - id: QA-H0046-05
      requisito_violado: "§7.6 — fachada sem lógica substantiva"
      evidencia_focal: "A prova alternativa aceita falsos conformes como return delegado(x[0]), return delegado(42) e return estado.update(x); não garante encaminhamento direto dos argumentos nem ausência de mutação."
      impacto: "Um wrapper com transformação, argumento calculado ou mutação pode satisfazer a prova."
      correcao_necessaria: "Restringir a AST a delegação direta com argumentos preservados e alvo de delegação nominalmente permitido."
    - id: QA-H0046-06
      requisito_violado: "D-MOD-08 item 10 — localização direta das responsabilidades"
      evidencia_focal: "O mapa não inclui tela/renderizacao/__init__.py e usa apenas hasattr, sem comprovar que o símbolo é materializado ou definido no módulo proprietário. Além disso, a lista de reexportação omite consumidores reais de _quebrar_texto, _avaliar_regra_ativo, _texto_chip_barra e _texto_valor_campo."
      impacto: "Módulos ausentes ou responsabilidades importadas de outro lugar podem passar; a fachada pode quebrar consumidores preservados."
      correcao_necessaria: "Incluir __init__.py, verificar definição/propriedade efetiva e registrar/reexportar os símbolos externos reais."
  achados_novos: []
  verificacoes_focais:
    - "Demonstração estrutural executada com carregar_estilo, tela demo existente, renderizar_tela e geometria_console; altura 40 passou em larguras 80 e 42, com coerência dimensional."
    - "Smoke demo.py --help executado sem erro e sem interação."
    - "Seis blocos Python heredoc do handoff validados sintaticamente."
    - "Como tela/renderizacao/ ainda não existe, o detector de ciclos e o mapa executável não foram executados."
  status: H2_HANDOFF_PATCH_REQUIRED
  bloqueios: []
```
