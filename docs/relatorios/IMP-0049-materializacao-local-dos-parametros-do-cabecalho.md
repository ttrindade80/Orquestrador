# IMP-0049 — materialização local dos parâmetros do cabeçalho

```yaml
status: IMPLEMENTATION_COMPLETED
handoff: H-0049

baseline:
  branch: master
  head: 19085f420bf4dc0c2f094a809febac0933b25f77
  worktree_inicial: "92 arquivos rastreados modificados, sem stage, mais handoff/relatórios e __pycache__ não rastreados"
  alteracoes_parciais_encontradas:
    - "72 JSONs já tinham apresentacao, mas descricao.capitalizacao estava em inicio_de_frase"
    - "loader e renderer estavam parciais; o modelo já transportava cabecalho como dict"
    - "fixtures preexistentes dos 11 arquivos adicionais já tinham recebido apresentacao"
  alteracoes_parciais_preservadas:
    - "documentos de contrato, nomenclatura, handoff e QAs anteriores"
    - "modelo, fluxo de dados, testes e alterações válidas já presentes no worktree"

jsons:
  total: 80
  estruturais_migrados: 72
  descricao_preservar: 72
  descricao_inicio_de_frase_no_baseline: 0
  caminhos_estruturais:
    - config/telas/demo/demo.json
    - config/telas/demo/destino_minimo.json
    - config/telas/demo/grupo_minimo.json
    - config/telas/demo/h0029_dashboard_fracao.json
    - config/telas/demo/h0029_dashboard_igual.json
    - config/telas/demo/h0029_dashboard_percentual.json
    - config/telas/demo/h0029_grupo_fracao.json
    - config/telas/demo/h0029_grupo_igual.json
    - config/telas/demo/h0029_grupo_pai_distribuido.json
    - config/telas/demo/h0029_grupo_percentual.json
    - config/telas/demo/h0030_console_unico.json
    - config/telas/demo/h0030_dashboard_unico.json
    - config/telas/demo/h0030_matriz_2x2.json
    - config/telas/demo/h0030_matriz_2x4.json
    - config/telas/demo/h0030_matriz_3x2.json
    - config/telas/demo/h0035_catalogo.json
    - config/telas/demo/h0035_centralizado_h_colunas.json
    - config/telas/demo/h0035_console_com.json
    - config/telas/demo/h0035_console_sem.json
    - config/telas/demo/h0035_dashboard_com.json
    - config/telas/demo/h0035_dashboard_sem.json
    - config/telas/demo/h0035_esquerda_margens_min_max.json
    - config/telas/demo/h0035_h_margens_limitadas.json
    - config/telas/demo/h0035_h_uniforme.json
    - config/telas/demo/h0035_lancador_com.json
    - config/telas/demo/h0035_lancador_sem.json
    - config/telas/demo/h0035_matriz_fixa_cabe.json
    - config/telas/demo/h0035_matriz_fixa_quadro_minimo.json
    - config/telas/demo/h0035_minimo_fixo_excedido.json
    - config/telas/demo/h0035_pref_colunas.json
    - config/telas/demo/h0035_pref_linhas.json
    - config/telas/demo/h0035_quatro_centralizados.json
    - config/telas/demo/h0035_resto_horizontal.json
    - config/telas/demo/h0035_resto_vertical.json
    - config/telas/demo/h0035_tres_centralizados.json
    - config/telas/demo/h0035_um_centralizado.json
    - config/telas/demo/h0035_uma_coluna.json
    - config/telas/demo/h0035_uma_linha.json
    - config/telas/demo/h0035_v_margens_min.json
    - config/telas/demo/h0035_v_margens_min_max.json
    - config/telas/demo/h0035_v_uniforme.json
    - config/telas/demo/h0036_console_conjuntos.json
    - config/telas/demo/h0036_console_hierarquia.json
    - config/telas/demo/h0036_console_tabela.json
    - config/telas/demo/h0037_console_alternavel_tres_niveis.json
    - config/telas/demo/h0037_console_nao_verboso.json
    - config/telas/demo/h0037_console_tabela_alternavel.json
    - config/telas/demo/h0037_console_verboso_dois_niveis.json
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - config/telas/demo/h0041_selecao_multipla_oito_itens.json
    - config/telas/demo/h0044_fluxo_execucao_integrado.json
    - config/telas/demo/h0045_dois_consoles_paginas_independentes.json
    - config/telas/demo/h0045_fluxo_execucao_paginado.json
    - config/telas/demo/h0045_paginacao_conjunto_vazio.json
    - config/telas/demo/h0045_paginacao_console_unico.json
    - config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
    - config/telas/demo/h0045_paginacao_politicas_quebra.json
    - config/telas/demo/h0045_validacao_continuacao.json
    - config/telas/demo/h0045_validacao_fluxo_continuo.json
    - config/telas/demo/h0045_validacao_manter_junto.json
    - config/telas/demo/h0045_validacao_nova_pagina.json
    - config/telas/demo/h0045_validacao_vazio.json
    - config/telas/demo/resultado_execucao.json
    - config/telas/demo/stub_b.json
  conteudos_externos_preservados:
    - config/telas/demo/h0035_console_com_conteudo.json
    - config/telas/demo/h0035_console_sem_conteudo.json
    - config/telas/demo/h0036_conjuntos_conteudo.json
    - config/telas/demo/h0036_hierarquia_conteudo.json
    - config/telas/demo/h0036_tabela_conteudo.json
    - config/telas/demo/h0037_dois_niveis_conteudo.json
    - config/telas/demo/h0037_tabela_conteudo.json
    - config/telas/demo/h0037_tres_niveis_conteudo.json
  hashes_de_preservacao_verificados: true

baseline_migratorio_final:
  titulo:
    capitalizacao: maiusculas
  descricao:
    capitalizacao: preservar
  geometria:
    recuo_lateral: 0
    recuo: 1

implementacao:
  codigo:
    - "tela/carregamento/tela_json.py: schema fechado, tipos, enums, inteiros não booleanos e limites"
    - "tela/renderizacao/geometria_caixa.py: preservacao, inicio_de_frase, maiusculas e oito parâmetros"
    - "tela/renderizacao/tela.py: consumo local em cálculo e renderização do cabeçalho"
    - "tela/modelo.py: transporte integral já existente verificado e preservado"
  hardcodings_removidos: "upper incondicional do cabeçalho, posição/alinhamento/recuos/formato fixos e leitura global obsoleta"
  fallback_removido: "ausência de apresentação não recebe default; o cabeçalho usa somente o bloco validado"
  arquivo_removido: config/elementos/cabecalho.json

preservacao_observavel:
  fixture_desc_fab:
    entrada: "desc fab"
    resultado: "desc fab"
    expectativa_alterada: false
  telas_auditadas: 72
  telas_que_mudariam_com_inicio_de_frase: 17

fixtures_preexistentes:
  ocorrencias_incompativeis_antes: 58
  arquivos_com_ocorrencias_antes: 13
  arquivos_adicionados_ao_manifesto: 11
  ocorrencias_incompativeis_restantes: 0
  ocorrencias_com_baseline_inicio_de_frase: 0
  novas_fixtures_criadas: 0
  fixtures_persistentes_criadas: 0
  novos_testes_criados: 0
  testes_removidos: 0
  testes_renomeados: 0
  testes_ignorados: 0
  assercoes_funcionais_alteradas: 0
  expectativas_alteradas: 0
  arquivos_adicionais_adequados:
    - tela/teste_resultado_execucao.py
    - tela/teste_navegacao.py
    - tela/testes_renderizador/integracao.py
    - tela/testes_renderizador/composicao_corpo.py
    - tela/testes_renderizador/comum.py
    - tela/testes_renderizador/lancador.py
    - tela/testes_renderizador/matriz_participantes.py
    - tela/testes_renderizador/selecao.py
    - demo/teste_demo_navegacao.py
    - demo/teste_demo_paginacao.py
    - demo/teste_diagnostico.py

validacao:
  teste_desc_fab: "1 passado, resultado observado desc fab"
  testes_focais_h0049: "26 loader, 2 modelo e 6 renderer passados"
  teste_dos_onze_arquivos: "514 passados; coleta preservada"
  suite_integral: "998 passados"
  quantidade_coletada: 998
  falhas: 0
  erros: 0
  hashes_ok: 8
  consumidores_residuais: 0
  diff_check: aprovado
  inventario_fixture_ast: "58 antes; 0 incompatíveis restantes; negativas intencionais separadas"
  auditoria_baseline_json: "72 auditados; preservar=72; inicio_de_frase=0; ausentes=0; outros=0"
  negativas_intencionais_h0049:
    quantidade: 4
    testes:
      - tela/teste_loader.py::test_h0049_loader_schema_completo_e_preservacao_integral
      - tela/teste_loader.py::test_h0049_loader_tipos_e_enumeracoes_rejeitados
      - tela/teste_loader.py::test_h0049_loader_max_caracteres_rejeita_fora_do_dominio
      - tela/teste_loader.py::test_h0049_loader_limites_inclusivos_recuos_zero_e_sem_fallback
  bloqueios: []
```

As alterações ficaram restritas ao manifesto transportado pelo H-0049, sem
stage ou commit. `config/estilo.json`, conteúdos externos, contratos e
relatórios anteriores foram preservados.
