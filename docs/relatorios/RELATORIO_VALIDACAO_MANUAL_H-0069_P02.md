# Relatório de Validação Manual — H-0069 P02

```yaml
rastreabilidade:
  etapa: VALIDACAO_MANUAL
  objeto: H-0069
  patch: P02
  item: ITEM-0010
  adr: ADR-0046
  evidencias:
    historica_falha_pre_p02:
      docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0069.md
    qa_pos_patch_p02:
      docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0069_P02.md

contexto_tecnico_anterior:
  qa_pos_patch_p02: I1_IMPLEMENTATION_APPROVED
  revalidacao_manual_tty_real: OBRIGATORIA

execucao_informada:
  operador: usuário
  ambiente: TTY real
  comando:
    - 'cd "$(git rev-parse --show-toplevel)" || return 1'
    - 'python demo/demo.py'

percurso_revalidado:
  - F4
  - tela Estilo
  - alterar preset de borda
  - Aplicar
  - demonstração integrada
  - popup
  - CONFIRMADO

resultado_literal_do_usuario: "tudo funcionou"

crash_anterior_caminho_CONFIRMADO:
  reapareceu: false

caminho_ABORTADO:
  validado_pelo_usuario: true
  resultado_literal_do_usuario: "tudo funcionou"

resultado:
  status: MANUAL_VALIDATION_APPROVED

validacao_funcional:
  CONFIRMADO:
    status: APROVADO
    crash_runtime: AUSENTE
    retorno_a_Estilo: CORRETO
  ABORTADO:
    status: APROVADO
    crash_runtime: AUSENTE
    retorno_a_Estilo: CORRETO
  demonstracao_integrada:
    status: APROVADA_FUNCIONALMENTE

classificacao_H0069: TECNICAMENTE_E_MANUALMENTE_APROVADO

refinamentos_visuais:
  status: ESCOPO_FECHADO_PARA_NOVO_HANDOFF
  natureza:
    - apresentacao_dos_filhos
    - alinhamento_de_amostras
    - chips_multitecla
    - aplicacao_real_de_estilos_na_barra_de_menus
  nao_classificar_como: regressao_do_P02
  nao_invalidam: aprovacao_funcional_H0069

escopo_fechado_continuidade:
  filhos_tela_estilo:
    estado_atual: ordinal_alfabetico_A_B_C
    decisoes:
      - remover o ordinal alfabético dos filhos
      - não renderizar A), B), C) etc.
      - preservar a indentação hierárquica
      - o cursor de navegação do filho deve ocupar a região horizontal hoje usada pelo ordinal
      - preservar o indicador visual do preset vigente/não vigente
      - o texto dos presets deve permanecer alinhado
  alinhamento_das_amostras:
    regra: amostras visuais de uma mesma categoria devem começar na mesma coluna
    exemplo_conceitual:
      - "Borda Curva  <amostra>"
      - "Borda Reta   <amostra>"
      - "Linha        <amostra>"
    decisoes:
      - calcular a maior largura visual do nome entre os filhos comparados
      - completar nomes menores com espaços
      - iniciar todas as amostras na mesma coluna visual
      - usar largura visual efetiva
      - não usar comprimento bruto de ANSI/CSI como largura
  chips_de_uma_tecla:
    decisoes:
      - chips de uma única tecla não mudam
      - preservar a representação atual de todos os presets
  chips_multitecla_presets_delimitados:
    comportamento: preservar o comportamento atual
    exemplo: "[PgUp][PgDn] Páginas"
    nao_introduzir: barra "/"
  chip_multitecla_ponto:
    uma_tecla: permanece como atualmente definido
    multiplas_teclas_mesma_acao: um único chip textual
    representacao: " PgUp/PgDn."
    semantica_material:
      - espaço inicial pertence à representação
      - PgUp e PgDn são separados por "/"
      - um único ponto encerra o conjunto
      - depois vem o espaçamento normal entre chip e descrição da ação
  chip_multitecla_destaque_texto:
    tratamento: PgUp/PgDn como um único chip multitecla
    representacao: " PgUp/PgDn "
    regras:
      - existe espaço lateral visível antes e depois
      - a cor de texto aplica-se ao conteúdo PgUp/PgDn
      - os espaços laterais não precisam receber efeito visual de cor
      - a largura visual total inclui os espaços laterais
  chip_multitecla_destaque_fundo:
    tratamento: PgUp/PgDn como um único chip multitecla
    representacao: " PgUp/PgDn "
    regras:
      - o fundo deve abranger o chip inteiro
      - incluir os espaços laterais no fundo
      - o resultado deve formar visualmente uma única unidade retangular
      - a largura visual total inclui os espaços laterais
  barra_de_menus:
    aplicar_aos_chips_reais:
      - Ponto
      - Destaque Texto
      - Destaque Fundo
    nao_limitar: amostras da tela Estilo
    decisoes:
      - materializar os chips pelo preset vigente
      - preservar o texto da ação como parte semanticamente separada do chip
      - manter alinhamento correto independentemente do preset
      - calcular geometria por largura visual efetiva
      - tratar ANSI de cor/fundo como largura zero
      - contar espaços visíveis normalmente
      - recalcular alinhamento quando o estilo mudar em runtime
      - preservar alinhamento após resize
    nao_altera: ordem lógica dos itens da Barra de Menus
    fora_deste_trabalho: reorganização global de posição/ordem da Barra

gates:
  validacao_manual_H0069:
    status: MANUAL_VALIDATION_APPROVED
  validacao_manual_final_ITEM0010:
    status: PENDENTE
    motivo: refinamentos_visuais_a_implementar_e_revalidar

proxima_acao: CRIAR_HANDOFF_H0070
capacidade_prevista: >
  refinamentos finais de apresentação do Estilo e aplicação dos estilos de
  chip na Barra de Menus

nao_executado_nesta_etapa:
  - criacao_H0070
  - alteracao_de_codigo
  - QA
  - implementacao_dos_refinamentos
  - alteracao_de_config_estilo_json
  - nova_validacao_manual
  - fechamento_ITEM0010
  - stage
  - commit
  - push
```

Registro documental da revalidação manual H-0069 pós-P02 executada pelo
usuário em TTY real com `python demo/demo.py`. O percurso F4 → tela Estilo →
alterar preset de borda → Aplicar → demonstração integrada → popup →
`CONFIRMADO` funcionou. O crash anteriormente observado no caminho
`CONFIRMADO` não reapareceu. O caminho `ABORTADO` também foi validado e
funcionou. Resultado: `MANUAL_VALIDATION_APPROVED`. H-0069 fica
`TECNICAMENTE_E_MANUALMENTE_APROVADO`. Refinamentos visuais de apresentação
dos filhos, alinhamento de amostras, chips multitecla e aplicação real dos
estilos na Barra de Menus ficam como escopo fechado para novo handoff e não
são regressão do P02. Validação manual final do ITEM-0010 permanece
`PENDENTE`. Próxima ação: `CRIAR_HANDOFF_H0070`.
