# Relatorio de QA do handoff H-0033

```yaml
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: PATCH_HANDOFF
relatorio: docs/relatorios/RELATORIO_QA_H-0033_HANDOFF.md
handoff_auditado: docs/handoff/H-0033-ocupacao-integral-corpo.md
adr_aplicavel: docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
qa_aplicacao_adr: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0024.md

cronologia_H_0033:
  resultado: PARCIALMENTE_CONFORME
  evidencia:
    - "H-0033 existe como arquivo novo e registra metadata.id=H-0033 e data_criacao=2026-07-16."
    - "docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md ja existe no checkout."
    - "O handoff declara que H-0033 foi criado agora e e cronologicamente posterior ao H-0034 existente."
    - "Nao foi encontrada declaracao de commit do H-0033."
  ressalva: >
    A frase "apos o fechamento do ciclo ADR-0024" e imprecisa porque o Git ainda
    contem alteracoes acumuladas da ADR-0024 nao commitadas. O proprio handoff
    lista essas alteracoes e proibe commit, portanto a imprecisao nao chega a
    afirmar fechamento Git, mas deve ser ajustada para evitar ambiguidade de
    rastreabilidade.

separacao_de_escopos:
  resultado: CONFIRMADO
  autor_CRIAR_HANDOFF:
    - docs/handoff/H-0033-ocupacao-integral-corpo.md
  futura_implementacao:
    codigo:
      - tela/renderizador.py
      - tela/modelo.py
      - tela/loader.py
    testes:
      - tela/teste_renderizador.py
      - tela/teste_loader.py
      - tela/teste_modelo.py
      - demo/teste_demo.py
      - demo/teste_diagnostico.py
      - demo/teste_explorar_barra_de_menus.py
    demonstracao:
      - demo/demo.py
      - demo/diagnostico.py
    relatorio:
      - docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
  observacao: "A restricao de arquivo unico nao foi transferida para a implementacao futura."

capacidade_coesa:
  resultado: CONFIRMADO
  capacidade: "aplicacao tecnica da ADR-0024 para ocupacao integral da area do corpo e containers estruturais"
  fora_de_escopo_preservado:
    - cabecalho com quebra ou reticencias
    - responsividade do lancador ja tratada no H-0034
    - nova arquitetura de distribuicao
    - mudanca de tipos visuais
    - renumeracao de handoffs
    - commit

inventario_jsons:
  quantidade_declarada: 16
  quantidade_confirmada: 16
  omitidos: []
  indevidamente_incluidos: []
  exclusoes_auditadas:
    docs/relatorios/anexos/orquestrador_stub_b_validacao.json:
      resultado: CONFIRMADO
      evidencia:
        - "schema=tela.v1"
        - "metadados.status=draft"
        - "nao apareceu em referencias de tela/, demo/ ou config/telas"
        - "referencias encontradas somente em relatorios e no proprio handoff"
  descoberta_independente:
    git_ls_files_json: "16 JSONs de tela em config/telas/demo/; demais JSONs sao estilo, elementos, layouts ou anexo historico."
    rg_files_json: "Mesmo conjunto rastreado, incluindo anexo em docs/relatorios/anexos."
    config_telas_fora_demo: []
  qualidade_da_tabela:
    resultado: CONFIRMADO_COM_DEFEITO_DE_ACAO
    campos_presentes:
      - caminho
      - identidade da tela
      - uso
      - estrutura do corpo
      - distribuicao atual
      - avaliacao inicial
      - acao autorizada
    defeito: "Tres JSONs classificados como INCOMPATIVEL recebem acao REVISAR_E_PRESERVAR."

arquivos_futura_implementacao:
  codigo:
    resultado: CONFIRMADO
    evidencia:
      - "tela/renderizador.py contem o bloco de fill externo em renderizar_tela, linhas atuais 1693-1708."
      - "tela/modelo.py e tela/loader.py possuem criterio condicional ligado a validacao estrutural DA-02/DA-04."
    ressalva: "A localizacao condicional e tecnica, nao cria decisao arquitetural nova."
  testes:
    resultado: CONFIRMADO
    evidencia:
      - "Os seis arquivos declarados compoem a suite executada e somam 1937 verificacoes."
      - "Nao foi localizado outro arquivo de teste obrigatorio para preservar a baseline declarada."
  jsons:
    resultado: PATCH_REQUIRED
    evidencia:
      - "Todos os 16 caminhos estao nominalmente autorizados."
      - "A regra de acao para os tres INCOMPATIVEL e contraditoria com a propria classificacao."
  demonstracao:
    resultado: CONFIRMADO_COM_RESSALVA
    evidencia:
      - "demo/demo.py e ponto de entrada real."
      - "demo/diagnostico.py fornece pipeline nao interativo."
      - "COLUMNS/LINES nao controlam dimensoes em TTY real quando ioctl retorna par valido."
  relatorio:
    resultado: CONFIRMADO
    caminho: docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
    evidencia: "O template contem entrada nominal para todos os 16 JSONs."

casos_obrigatorios:
  caso_A_destino_minimo:
    resultado: CONFIRMADO
    identidade:
      tela: destino_minimo
      dashboard: dashboard_teste
      titulo_dashboard: Teste
      cabecalho: Destino Minimo
    aceite: "ocupacao integral, ausencia de faixa externa, preservacao de espaco interno legitimo"
  caso_B_grupo_minimo:
    resultado: CONFIRMADO
    identidade:
      tela: grupo_minimo
      grupo: grupo_principal
      dashboard: dashboard_conteudo
      titulo_dashboard: Conteudo
      dashboard_TESTE: INEXISTENTE
    aceite: "DA-01 e DA-03 aplicadas conjuntamente"
  caso_C_multiplos_sem_distribuicao:
    resultado: CONFIRMADO
    evidencia: "Handoff autoriza fixture invalida nominal dentro dos testes autorizados, sem transformar configuracao permanente valida em invalida."
  caso_D_distribuicao_explicita_valida:
    resultado: CONFIRMADO
    evidencia: "config/telas/demo/demo.json: id=demo, corpo vertical, distribuicao fracao [2,1,2], tres elementos."
    ressalva: "O marcador de titulo real e Orquestrador, nao Demo; o handoff permite 'ou equivalente'."
  caso_E_container_aninhado:
    resultado: CONFIRMADO
    evidencia: "grupo_minimo e fixtures h0029_grupo_* cobrem propagacao por grupo."

demonstracao_real:
  resultado: PATCH_REQUIRED
  achado: QA-H0033-HIGH-002
  evidencia:
    - "demo/demo.py usa _obter_dimensoes_iniciais: ioctl(TIOCGWINSZ) primeiro, env COLUMNS/LINES apenas se ioctl falhar ou for invalido."
    - "Em TTY real valido, COLUMNS=42 LINES=20 python demo/demo.py nao garante 42x20; pode exigir redimensionamento fisico ou PTY controlado."
    - "As teclas d e g realmente selecionam destino_minimo e grupo_minimo a partir de demo.json."
  conclusao: "Os comandos sao parcialmente reproduziveis, mas a declaracao de que COLUMNS/LINES definem dimensoes em TTY real e falsa no ponto de entrada atual."

suite_canonica:
  resultado: CONFIRMADO
  comandos_executados:
    tela/teste_renderizador.py:
      comando: python tela/teste_renderizador.py
      verificacoes: 1065
      passaram: 1065
      falharam: 0
    tela/teste_loader.py:
      comando: python tela/teste_loader.py
      verificacoes: 283
      passaram: 283
      falharam: 0
    tela/teste_modelo.py:
      comando: python tela/teste_modelo.py
      verificacoes: 163
      passaram: 163
      falharam: 0
    demo/teste_demo.py:
      comando: python demo/teste_demo.py
      verificacoes: 358
      passaram: 358
      falharam: 0
    demo/teste_diagnostico.py:
      comando: python demo/teste_diagnostico.py
      verificacoes: 30
      passaram: 30
      falharam: 0
    demo/teste_explorar_barra_de_menus.py:
      comando: python demo/teste_explorar_barra_de_menus.py
      verificacoes: 38
      passaram: 38
      falharam: 0
  total: 1937
  erro: false

validacao_manual:
  resultado: CONFIRMADO
  status_requerido: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
  executor_nao_autorizado_a_aprovar: true
  cobre:
    - TTY real
    - destino_minimo
    - grupo_minimo
    - dashboard Conteudo
    - 42x20
    - 80x30
    - redimensionamento
    - barra_de_menus
    - rejeicao explicita de configuracoes invalidas

teste_inventario:
  resultado: CONFIRMADO
  evidencia: "Handoff exige verificacao automatizada que compare conjunto real de JSONs em config/telas/demo/ com conjunto registrado no relatorio de implementacao."
  exequivel_com_arquivos_autorizados: true

relatorio_implementacao:
  resultado: CONFIRMADO
  evidencia:
    - "Arquivo autorizado nominalmente."
    - "Template contem entrada nominal para cada JSON."
    - "Inclui DA-01 a DA-04, suite, demonstracao, validacao manual pendente e excecoes operacionais."
  ressalva: "Nao deve autoaprovar formalmente a implementacao; o handoff declara essa proibicao."

excecao_operacional:
  resultado: CONFIRMADO
  evidencia:
    - "Arquivo fora da lista nao pode ser alterado silenciosamente."
    - "Executor deve parar antes, informar arquivo, motivo, escopo e mudanca esperada."
    - "Exige autorizacao explicita e nao permite nova arquitetura, semantica ou politica."

verificacao_exequibilidade:
  - item: 1
    declaracao_do_handoff: "Todos os JSONs de telas foram inventariados: 16 arquivos; anexo excluido por draft nao referenciado."
    evidencia: "git ls-files e rg --files confirmaram os 16 JSONs em config/telas/demo/; anexo tem metadados.status=draft e referencias apenas documentais."
    resultado: CONFIRMADO
  - item: 2
    declaracao_do_handoff: "Cada JSON aparece nominalmente nas permissoes ou preservacoes."
    evidencia: "Todos os 16 aparecem na tabela 9.2 e na lista 10.3."
    resultado: CONFIRMADO
  - item: 3
    declaracao_do_handoff: "Todos os incompatíveis podem ser atualizados no H-0033."
    evidencia: "Os tres marcados INCOMPATIVEL sao autorizados na lista 10.3, mas a acao da tabela e REVISAR_E_PRESERVAR."
    resultado: CONTRADITORIO
  - item: 4
    declaracao_do_handoff: "Codigo, testes, demonstracao e relatorio possuem arquivos autorizados."
    evidencia: "Secao 10 lista os arquivos nominalmente."
    resultado: CONFIRMADO
  - item: 5
    declaracao_do_handoff: "Nenhum arquivo necessario esta simultaneamente proibido."
    evidencia: "Arquivos de codigo/teste/demo/IMP nao aparecem na secao 11 de preservacao."
    resultado: CONFIRMADO
  - item: 6
    declaracao_do_handoff: "Suite canonica pode ser atualizada e executada."
    evidencia: "Seis arquivos de teste autorizados; todos executados com 1937/1937."
    resultado: CONFIRMADO
  - item: 7
    declaracao_do_handoff: "destino_minimo e grupo_minimo podem ser demonstrados pelo ponto de entrada real."
    evidencia: "demo.py carrega demo e processa chips d/g; comandos de dimensao tem problema em TTY real por precedencia de ioctl."
    resultado: CONTRADITORIO
  - item: 8
    declaracao_do_handoff: "Existe prova para composicao invalida via fixture nominal nos testes."
    evidencia: "Caso C autoriza fixture invalida nominal dentro de teste autorizado."
    resultado: CONFIRMADO
  - item: 9
    declaracao_do_handoff: "Existe prova para composicao valida com distribuicao."
    evidencia: "demo.json e h0029_* com distribuicao explicita existem e estao autorizados."
    resultado: CONFIRMADO
  - item: 10
    declaracao_do_handoff: "Existe criterio independente para detectar espaco externo."
    evidencia: "AC-01/AC-02 e secao 16 distinguem linhas externas de espaco interno; testes proibem expectativa derivada da saida."
    resultado: CONFIRMADO
  - item: 11
    declaracao_do_handoff: "O relatorio pode registrar todo o inventario."
    evidencia: "Template da secao 20 possui entradas para os 16 JSONs."
    resultado: CONFIRMADO
  - item: 12
    declaracao_do_handoff: "Validacao humana em TTY real e reproduzivel; COLUMNS e LINES definem dimensoes."
    evidencia: "demo.py consulta ioctl antes de COLUMNS/LINES em TTY real."
    resultado: CONTRADITORIO
  - item: 13
    declaracao_do_handoff: "Nao existe decisao arquitetural pendente."
    evidencia: "ADR-0024 e contratos definem DA-01 a DA-04; detalhes tecnicos ficam para implementacao."
    resultado: CONFIRMADO
  - item: 14
    declaracao_do_handoff: "Escopo forma uma unica capacidade coesa."
    evidencia: "Escopo positivo/negativo e casos obrigatorios convergem para aplicacao tecnica da ADR-0024."
    resultado: CONFIRMADO

achados_bloqueantes: []

achados_altos:
  - id: QA-H0033-HIGH-001
    titulo: "JSONs classificados como INCOMPATIVEL autorizados apenas para preservacao"
    local:
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:305"
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:306"
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:307"
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:323-333"
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:1078-1081"
    evidencia: >
      destino_minimo.json, grupo_minimo.json e stub_b.json aparecem como
      INCOMPATIVEL, mas a acao autorizada na tabela e REVISAR_E_PRESERVAR.
      A justificativa posterior diz que a estrutura JSON e valida sob DA-01 e
      que o renderer precisa ser corrigido.
    impacto: >
      O handoff mistura incompatibilidade do comportamento atual do renderer com
      incompatibilidade do JSON. Isso viola a regra de que JSON classificado como
      incompatível nao pode ficar apenas autorizado para preservacao, e cria
      ambiguidade para o executor e para o relatorio de implementacao.
    correcao_esperada: >
      Ajustar classificacao e acao de modo coerente. Se os JSONs sao validos sob
      DA-01 e devem ser preservados, nao devem ser marcados como INCOMPATIVEL;
      se forem mantidos como INCOMPATIVEL, a acao nao pode ser somente preservar.
  - id: QA-H0033-HIGH-002
    titulo: "Comandos de demonstracao declaram dimensoes por COLUMNS/LINES que nao prevalecem em TTY real"
    local:
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:820-837"
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:1095-1097"
      - "demo/demo.py:390-398"
      - "demo/demo.py:522-525"
    evidencia: >
      O handoff manda executar COLUMNS=42 LINES=20 python demo/demo.py em TTY
      real. O codigo do ponto de entrada, em TTY, chama ioctl(TIOCGWINSZ)
      primeiro e usa COLUMNS/LINES apenas se ioctl nao fornecer par valido.
    impacto: >
      A validacao manual pode nao reproduzir 42x20/80x30 com os comandos
      declarados, e o item de exequibilidade 12 fica falso no ponto essencial
      de demonstracao real.
    correcao_esperada: >
      Corrigir o handoff para indicar redimensionamento fisico do terminal,
      execucao sob PTY controlado, ou comando/metodo que efetivamente imponha
      dimensoes no ponto de entrada real.

achados_medios:
  - id: QA-H0033-MED-001
    titulo: "Formula cronologica usa 'fechamento do ciclo ADR-0024' de forma ambigua"
    local:
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:73-75"
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:84-103"
    evidencia: >
      O handoff registra corretamente que ha alteracoes acumuladas da ADR-0024
      nao atribuidas ao autor do handoff e nao declara commit. Ainda assim, a
      expressao "fechamento do ciclo ADR-0024" pode ser lida como fechamento Git.
    impacto: "Risco medio de ambiguidade de rastreabilidade."
    correcao_esperada: "Explicitar que se trata de conclusao do fluxo documental aprovado, nao de ciclo Git commitado."

achados_baixos:
  - id: QA-H0033-LOW-001
    titulo: "Marcador semantico de demo.json e flexivel demais"
    local:
      - "docs/handoff/H-0033-ocupacao-integral-corpo.md:861"
    evidencia: "O JSON real tem cabecalho.titulo='Orquestrador', enquanto a tabela diz titulo 'Demo' ou equivalente."
    impacto: "Baixo; a propria formula aceita equivalente, mas a prova ficaria mais auditavel com o marcador real."
    correcao_esperada: "Usar explicitamente 'Orquestrador' como marcador esperado da tela demo."

observacoes:
  - "A ADR-0024, os contratos e a nomenclatura preservam DA-01 a DA-04 sem exigir nova arquitetura."
  - "Espaco interno dentro de moldura de elemento visual permanece permitido e o handoff registra essa distincao."
  - "A suite atual ainda contem expectativas de fill externo antigo; o handoff identifica que elas devem ser atualizadas."
  - "A validacao manual nao foi executada neste QA."

arquivos_observados:
  modificados_acumulados_adr_0024:
    - docs/NOMENCLATURA.md
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_tela_json.md
  nao_rastreados_antes_deste_relatorio:
    - docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
    - docs/handoff/H-0033-ocupacao-integral-corpo.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
    - docs/relatorios/RELATORIO_QA_ADR-0024.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0024.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md
  criado_por_este_QA:
    - docs/relatorios/RELATORIO_QA_H-0033_HANDOFF.md
  inesperados:
    - origem: NAO_CONFIRMADA
      produzido_pelo_executor: NAO_CONFIRMADO
      produzido_pelo_usuario: NAO_CONFIRMADO
      caminhos: []

git:
  git_status_short_antes_deste_relatorio: "Conforme lista acumulada da ADR-0024 + H-0033 novo; nenhum codigo, teste ou JSON alterado."
  git_diff_check: LIMPO
  git_diff_no_index_handoff: "codigo 1 esperado para arquivo novo comparado com /dev/null; diff mostrou somente o conteudo do handoff."
  suite_canonica_executada: "1937/1937"
  status_esperado_apos_relatorio:
    - "?? docs/relatorios/RELATORIO_QA_H-0033_HANDOFF.md"

proxima_categoria: PATCH_HANDOFF
```

## Conclusao

O H-0033 e substantivamente exequivel quanto a arquitetura da ADR-0024, ao
inventario nominal dos 16 JSONs, aos arquivos autorizados, a suite canonica e a
separacao de escopos. Entretanto, dois defeitos materiais impedem aprovacao do
handoff: a incoerencia entre classificacao `INCOMPATIVEL` e acao
`REVISAR_E_PRESERVAR` para tres JSONs, e a demonstracao real com dimensoes
declaradas por `COLUMNS`/`LINES` apesar de o ponto de entrada TTY priorizar
`ioctl`.

Classificacao formal: `H2_HANDOFF_PATCH_REQUIRED`.
