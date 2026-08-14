# Relatório de Validação Manual Final — ITEM-0010

```yaml
rastreabilidade:
  etapa: REGISTRAR_VALIDACAO_MANUAL_FINAL
  objeto: ITEM-0010
  item: ITEM-0010
  adr: ADR-0046
  handoff_mais_recente: H-0070
  evidencias:
    h0069_aprovacao_manual:
      docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0069_P02.md
    h0070_qa_pos_p01:
      docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0070_P01.md

estado_tecnico_atual:
  H-0069: tecnicamente_e_manualmente_aprovado
  H-0070: tecnicamente_aprovado_apos_P01
  validacao_manual_final_ITEM-0010: executada_e_reprovada

contexto_da_rodada:
  tipo: validacao_manual_final_integrada_do_ITEM-0010
  nota: >
    A aprovação técnica automatizada do H-0070 não substitui o gate visual
    humano.

execucao_evidenciada:
  operador: usuário
  ambiente: TTY real
  alvos_validados:
    - tela Estilo
    - Barra de Menus
  defeitos: residuais_informados_pelo_usuario
  descricao_material: fornecida_pelo_usuario
  captura_de_tela:
    fornecida: true
    uso: evidencia_visual_complementar_da_validacao_manual_final

resultado:
  status: MANUAL_VALIDATION_FAILED
  efeito_H0069: nao_invalida_funcionalmente
  efeito_ITEM0010: impede_fechamento_final

achados:
  - id: MF-ITEM0010-001
    titulo: composicao_multitecla_nao_atende_a_regra_visual_final
    resultado_observado:
      - em estilos com dois lados, o chip multitecla foi materializado de forma incorreta
      - exemplo_observado: "╭PgUp][PgDn╮"
      - apenas as bordas externas refletiram o novo estilo
      - a composicao interna preservou delimitadores incompativeis
    decisao_fechada_pelo_usuario_para_continuidade:
      unidade_visual: chips com mais de uma tecla formam uma unica unidade visual
      bordas: somente as extremidades externas recebem as bordas do estilo
      separador_interno: "/"
      abrangencia: vale uniformemente para todos os modelos multitecla
      exemplos_conceituais:
        - "[PgUp/PgDn]"
        - "╭PgUp/PgDn╮"
        - "(PgUp/PgDn)"
        - "-PgUp/PgDn-"
      preset_ponto:
        par_visual: espaco_a_esquerda_e_ponto_a_direita
        exemplo_multitecla: "PgUp/PgDn."
        nao_preservar: delimitadores internos entre PgUp e PgDn
    natureza:
      - defeito_visual
      - composicao_multitecla
      - decisao_visual_fechada_para_continuidade

  - id: MF-ITEM0010-002
    titulo: estilos_de_cor_fundo_nao_aplicados_corretamente_na_Barra_de_Menus_real
    resultado_observado:
      - os chips de cor/destaque nao estao sendo aplicados corretamente na Barra de Menus real
    decisao_fechada_pelo_usuario_para_continuidade:
      - os estilos de cor/fundo devem ser efetivamente materializados na Barra de Menus real
      - nao basta funcionar apenas nas amostras da tela Estilo
      - chips multitecla de cor tambem seguem a unidade unica com /
      - os modelos de cor usam espacos laterais como parte da composicao visual
    formulacao_factual_informada_pelo_usuario:
      - "o . fica com o par ' ' e '.' (espaço e ponto)"
      - "a cor tem espaço no lado direito e no lado esquerdo"
      - "a cor na letra tem espaço no lado esquerdo na cor do terminal e no lado direito na cor de destaque do fundo"
    limite:
      nao_inventar_implementacao_concreta_alem_dessa_evidencia
    natureza:
      - defeito_visual
      - barra_menus_real
      - estilos_cor_fundo
      - decisao_visual_fechada_para_continuidade

  - id: MF-ITEM0010-003
    titulo: ordem_e_indentacao_de_cursor_toggle_e_texto_incorretas
    resultado_observado_tela_estilo:
      - o cursor esta em posicao hierarquica incorreta
      - o toggle de selecao esta ainda mais a esquerda
      - a indentacao foi aplicada ao texto, e nao ao prefixo visual completo da linha filha
      - o cursor aparece no mesmo nivel visual do numero do nivel pai
    decisao_fechada_pelo_usuario:
      ordem_visual:
        1: cursor
        2: toggle_selecao
        3: texto
      regras:
        - a indentacao deve ser aplicada ao prefixo visual da linha filha
        - cursor e toggle devem pertencer ao nivel hierarquico do filho
        - o texto nao deve ser deslocado isoladamente para compensar cursor/toggle
        - a linha deve manter a ordem cursor, toggle_selecao, texto
    natureza:
      - defeito_visual
      - geometria_hierarquica
      - cursor_toggle
      - decisao_visual_fechada_para_continuidade

evidencia_visual:
  origem: captura_fornecida_pelo_usuario
  mostra_entre_outros_pontos:
    - composicao de chip Curva multitecla semelhante a "╭PgUp][PgDn╮"
    - cursor de filho desalinhado em relacao ao nivel hierarquico
    - toggle de selecao posicionado a esquerda do cursor
    - texto do filho recebendo indentacao que nao corresponde ao prefixo visual esperado
    - Barra de Menus sem aplicacao satisfatoria dos estilos de cor/fundo segundo a validacao humana
  limites:
    - nao_derivar_medidas_em_colunas_da_imagem
    - nao_declarar_causa_de_codigo_apenas_pela_captura

conclusao:
  H0069_funcional: PRESERVADO
  H0070_tecnico: PRESERVADO
  validacao_manual_final_ITEM0010: MANUAL_VALIDATION_FAILED
  fechamento_final_ITEM0010: BLOQUEADO_POR_VALIDACAO_MANUAL
  natureza: refinamentos_visuais_residuais_com_decisoes_fechadas_do_usuario
  nota: >
    A aprovação técnica automatizada do H-0070 não substitui o gate visual
    humano.

proxima_acao: CRIAR_HANDOFF_H0071
capacidade_prevista_do_proximo_handoff:
  - normalizacao final da composicao dos chips multitecla
  - aplicacao correta dos estilos de cor/fundo na Barra de Menus real
  - correcao da geometria hierarquica cursor, toggle_selecao, texto dos filhos da tela Estilo

nao_executado_nesta_etapa:
  - criacao_H0071
  - alteracao_de_codigo
  - QA
  - implementacao
  - alteracao_de_config_estilo_json
  - alteracao_de_ADR_contratos_nomenclatura_ou_backlog
  - fechamento_ITEM0010
  - stage
  - commit
  - push
```

Registro documental da validação manual final integrada do ITEM-0010,
executada pelo usuário em TTY real sobre a tela Estilo e a Barra de Menus.
A captura de tela fornecida pelo usuário foi usada como evidência visual
complementar. Resultado: `MANUAL_VALIDATION_FAILED`. A falha não invalida
funcionalmente o H-0069 e não altera a aprovação técnica do H-0070 após P01.
A falha impede o fechamento final do ITEM-0010. Achados: `MF-ITEM0010-001`
(composição multitecla), `MF-ITEM0010-002` (estilos de cor/fundo na Barra de
Menus real) e `MF-ITEM0010-003` (geometria hierárquica cursor, toggle e
texto). Próxima ação: `CRIAR_HANDOFF_H0071`.
