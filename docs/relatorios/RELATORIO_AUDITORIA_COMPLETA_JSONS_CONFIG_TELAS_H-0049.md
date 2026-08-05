# Auditoria completa dos JSONs de `config/telas` — H-0049

```yaml
status: AUDITORIA_CLASSIFICACAO_CONCLUIDA
resumo:
  total_jsons: 80
  telas_estruturais: 72
  dados_externos_de_componente: 8
  artefatos_auxiliares_nao_tela: 0
  artefatos_nao_referenciados: 0
  inconclusivos: 0
  jsons_invalidos: 0
impacto_h0049:
  manifesto_atual_confiavel: false
  contagem_corrigida: 72
  arquivos_a_remover_do_manifesto:
    - config/telas/demo/h0036_tabela_conteudo.json
    - config/telas/demo/h0037_tabela_conteudo.json
  arquivos_a_adicionar_ao_manifesto: []
  arquivos_a_preservar: 8
  patch_pode_ser_criado: true
```

## Critério e evidências

A descoberta fechada foi `find config/telas -type f -name '*.json' -print |
sort`, resultando em 80 caminhos. Todos foram decodificados integralmente com
`json.loads`; não há raiz inválida. A tabela mecânica registrou somente objetos
JSON, mas a forma da raiz separa dois contratos:

| Código | Raiz e chaves exatas |
|---|---|
| S0 | `object`: `barra_de_menus,cabecalho,corpo,id,schema` |
| S1 | `object`: S0 + `metadados` |
| S2 | `object`: S0 + `perfil` |
| S3 | `object`: `barra_de_menus,bindings,cabecalho,corpo,filtros,id,metadados,referencias_de_acoes,schema` |
| D0 | `object`: `dados,formato,tipo` |

O teste estrutural usou o caminho público documentado:
`carregar_tela(None, caminho.stem, raiz_telas="config/telas/demo")`. Os 72
arquivos S0–S3 foram `ACEITO`. Os oito D0 foram `REJEITADO` por
`TelaCampoObrigatorioAusente: schema`, exatamente porque não são raízes de
tela. O teste complementar usou `carregar_conteudo_externo` para os oito D0;
todos foram aceitos e validados.

`carregar_tela` constrói dinamicamente
`<raiz_telas>/<id_tela>.json` (`tela/carregamento/tela_json.py:101-145`),
valida `schema`, `id`, `cabecalho`, `corpo` e `barra_de_menus`
(`:173-207`) e devolve o documento em `_raw` (`:305-317`). Assim, a ausência de
uma ocorrência literal do nome não torna um JSON órfão. Os pontos de entrada
reais são:

* `T1`: `carregar_tela`, por ID e raiz;
* `T2`: `demo.demo._carregar_modelo_por_id`, que carrega a tela e chama
  `construir_modelo` (`demo/demo.py:1119-1141`);
* `T3`: `demo.demo_navegacao.carregar_modelo_por_caminho`, cujo resolvedor
  deriva raiz e nome-base de qualquer caminho explícito
  (`demo/demo_navegacao.py:56-103`), inclusive para arquivos sem referência
  nominal individual;
* `T4`: `tela.resultado_execucao.carregar_sessao_resultado`, para
  `resultado_execucao`;
* `T5`: integrações e testes que carregam IDs nominais, evidência adicional,
  não a autoridade do schema.

O catálogo `_CATALOGO_CONTEUDO_EXTERNO` é a referência de entrada dos dados
externos (`demo/demo.py:163-175`). `id_conteudo_externo_de` resolve o nome-base;
`carregar_conteudo_externo` constrói o mesmo caminho relativo e valida o
documento (`tela/carregamento/conteudo_externo.py:645-697`). O modelo tipa o
documento e o propaga somente a elementos `console`
(`tela/modelo.py:244-297`); `tela.renderizacao.console._linhas_console` e
`_linhas_conteudo_externo` consomem as apresentações declaradas, sem abrir
JSON (`tela/renderizacao/console.py:7-31`).

## Matriz completa

`ACEITO` e `REJEITADO(schema)` são os resultados da tentativa estrutural
individual. Para telas, “migra” significa candidato a receber
`cabecalho.apresentacao`; para conteúdo, o arquivo permanece integralmente
fora da migração. Em todos os S0–S3, o campo `cabecalho` foi confirmado como
objeto com somente `titulo` e `descricao`, ambos strings.

| Caminho | Raiz/chaves | Loader estrutural | Consumidor comprovado / entrada | Classificação | Subtipo | Migra no H-0049? | Evidência |
|---|---|---|---|---|---|---|---|
| `config/telas/demo/demo.json` | S3 | ACEITO | T2; ID inicial e seleção por tela | TELA_ESTRUTURAL | — | SIM | `schema,id,cabecalho,corpo,barra_de_menus` |
| `config/telas/demo/destino_minimo.json` | S0 | ACEITO | T2; destino de navegação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; T5 |
| `config/telas/demo/grupo_minimo.json` | S0 | ACEITO | T2; destino de navegação/grupo | TELA_ESTRUTURAL | — | SIM | raiz estrutural; T5 |
| `config/telas/demo/h0029_dashboard_fracao.json` | S0 | ACEITO | T1/T5; integração matricial H-0029 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID coincide com arquivo |
| `config/telas/demo/h0029_dashboard_igual.json` | S0 | ACEITO | T1/T5; integração matricial H-0029 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID coincide com arquivo |
| `config/telas/demo/h0029_dashboard_percentual.json` | S0 | ACEITO | T1/T5; integração matricial H-0029 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID coincide com arquivo |
| `config/telas/demo/h0029_grupo_fracao.json` | S0 | ACEITO | T1/T5; integração matricial H-0029 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID coincide com arquivo |
| `config/telas/demo/h0029_grupo_igual.json` | S0 | ACEITO | T1/T5; integração matricial H-0029 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID coincide com arquivo |
| `config/telas/demo/h0029_grupo_pai_distribuido.json` | S0 | ACEITO | T1/T5; integração matricial H-0029 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID coincide com arquivo |
| `config/telas/demo/h0029_grupo_percentual.json` | S0 | ACEITO | T1/T5; integração matricial H-0029 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID coincide com arquivo |
| `config/telas/demo/h0030_console_unico.json` | S0 | ACEITO | T2/T5; catálogo e console H-0030 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado na demo |
| `config/telas/demo/h0030_dashboard_unico.json` | S0 | ACEITO | T2/T5; catálogo e dashboard H-0030 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado na demo |
| `config/telas/demo/h0030_matriz_2x2.json` | S0 | ACEITO | T2/T5; catálogo e matriz H-0030 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado na demo |
| `config/telas/demo/h0030_matriz_2x4.json` | S0 | ACEITO | T2/T5; catálogo e matriz H-0030 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado na demo |
| `config/telas/demo/h0030_matriz_3x2.json` | S0 | ACEITO | T2/T5; catálogo e matriz H-0030 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado na demo |
| `config/telas/demo/h0035_catalogo.json` | S0 | ACEITO | T2; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; entradas `tela_destino` |
| `config/telas/demo/h0035_centralizado_h_colunas.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_console_com.json` | S0 | ACEITO | T2; catálogo H-0035, console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; também entrada do conteúdo externo |
| `config/telas/demo/h0035_console_sem.json` | S0 | ACEITO | T2; catálogo H-0035, console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; também entrada do conteúdo externo |
| `config/telas/demo/h0035_dashboard_com.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_dashboard_sem.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_esquerda_margens_min_max.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_h_margens_limitadas.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_h_uniforme.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_lancador_com.json` | S0 | ACEITO | T2/T5; catálogo H-0035, lançador | TELA_ESTRUTURAL | — | SIM | raiz estrutural; loader carrega configuração de lançador quando aplicável |
| `config/telas/demo/h0035_lancador_sem.json` | S0 | ACEITO | T2/T5; catálogo H-0035, lançador | TELA_ESTRUTURAL | — | SIM | raiz estrutural; loader carrega configuração de lançador quando aplicável |
| `config/telas/demo/h0035_matriz_fixa_cabe.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_matriz_fixa_quadro_minimo.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_minimo_fixo_excedido.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_pref_colunas.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_pref_linhas.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_quatro_centralizados.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_resto_horizontal.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_resto_vertical.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_tres_centralizados.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_um_centralizado.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_uma_coluna.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_uma_linha.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_v_margens_min.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_v_margens_min_max.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_v_uniforme.json` | S0 | ACEITO | T2/T5; catálogo H-0035 | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção por ID |
| `config/telas/demo/h0035_console_com_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0035_console_com`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=hierarquia`; loader próprio aceito |
| `config/telas/demo/h0035_console_sem_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0035_console_sem`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=hierarquia`; loader próprio aceito |
| `config/telas/demo/h0036_conjuntos_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0036_console_conjuntos`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=conjuntos_campos`; loader próprio aceito |
| `config/telas/demo/h0036_console_conjuntos.json` | S0 | ACEITO | T2/C1; console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; catálogo externo separado |
| `config/telas/demo/h0036_console_hierarquia.json` | S0 | ACEITO | T2/C1; console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; catálogo externo separado |
| `config/telas/demo/h0036_console_tabela.json` | S0 | ACEITO | T2/C1; console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; catálogo externo separado |
| `config/telas/demo/h0036_hierarquia_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0036_console_hierarquia`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=hierarquia`; loader próprio aceito |
| `config/telas/demo/h0036_tabela_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0036_console_tabela`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=tabela`; loader próprio aceito |
| `config/telas/demo/h0037_console_alternavel_tres_niveis.json` | S0 | ACEITO | T2/C1; console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; política local separada do conteúdo |
| `config/telas/demo/h0037_console_nao_verboso.json` | S0 | ACEITO | T2/C1; console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; conteúdo compartilhado no catálogo |
| `config/telas/demo/h0037_console_tabela_alternavel.json` | S0 | ACEITO | T2/C1; console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; conteúdo separado |
| `config/telas/demo/h0037_console_verboso_dois_niveis.json` | S0 | ACEITO | T2/C1; console `con` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; conteúdo compartilhado no catálogo |
| `config/telas/demo/h0037_dois_niveis_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0037_console_nao_verboso` e `h0037_console_verboso_dois_niveis`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=hierarquia`; uma fonte, dois consumidores |
| `config/telas/demo/h0037_tabela_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0037_console_tabela_alternavel`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=tabela`; loader próprio aceito |
| `config/telas/demo/h0037_tres_niveis_conteudo.json` | D0 | REJEITADO(schema) | C1; `h0037_console_alternavel_tres_niveis`, console `con` | DADOS_EXTERNOS_DE_COMPONENTE | console | NÃO | `formato.apresentacao=hierarquia`; loader próprio aceito |
| `config/telas/demo/h0040_nav_console_grade_2x3.json` | S1 | ACEITO | T3; `--tela`/caminho explícito | TELA_ESTRUTURAL | — | SIM | `metadados` + raiz estrutural |
| `config/telas/demo/h0040_nav_console_nao_focalizavel.json` | S1 | ACEITO | T3; `--tela`/caminho explícito | TELA_ESTRUTURAL | — | SIM | alcançável por resolvedor dinâmico; não é órfão |
| `config/telas/demo/h0040_nav_console_unico_linear.json` | S1 | ACEITO | T3/T5; `--tela` e testes de navegação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID derivado do caminho |
| `config/telas/demo/h0040_nav_degenere_um_item.json` | S1 | ACEITO | T3; `--tela`/caminho explícito | TELA_ESTRUTURAL | — | SIM | alcançável por resolvedor dinâmico |
| `config/telas/demo/h0040_nav_degenere_uma_coluna.json` | S1 | ACEITO | T3; `--tela`/caminho explícito | TELA_ESTRUTURAL | — | SIM | alcançável por resolvedor dinâmico; não é órfão |
| `config/telas/demo/h0040_nav_degenere_uma_linha.json` | S1 | ACEITO | T3; `--tela`/caminho explícito | TELA_ESTRUTURAL | — | SIM | alcançável por resolvedor dinâmico; não é órfão |
| `config/telas/demo/h0040_nav_dois_consoles.json` | S1 | ACEITO | T3/T5; `--tela` e testes de navegação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID derivado do caminho |
| `config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json` | S1 | ACEITO | T3/T5; navegação/redimensionamento | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID derivado do caminho |
| `config/telas/demo/h0040_nav_tres_consoles_em_grupo.json` | S1 | ACEITO | T3/T5; navegação em grupo | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID derivado do caminho |
| `config/telas/demo/h0041_selecao_multipla_oito_itens.json` | S1 | ACEITO | T3; `demo_selecao --tela` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; seleção explícita por caminho |
| `config/telas/demo/h0044_fluxo_execucao_integrado.json` | S1 | ACEITO | T2/T4; `tela.fluxo_execucao` | TELA_ESTRUTURAL | — | SIM | raiz estrutural; fluxo integrado |
| `config/telas/demo/h0045_dois_consoles_paginas_independentes.json` | S1 | ACEITO | T2/T5; paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado no fluxo |
| `config/telas/demo/h0045_fluxo_execucao_paginado.json` | S1 | ACEITO | T2/T3/T5; paginação/navegação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID e casos resolvidos dinamicamente |
| `config/telas/demo/h0045_paginacao_conjunto_vazio.json` | S1 | ACEITO | T2/T5; paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado no fluxo |
| `config/telas/demo/h0045_paginacao_console_unico.json` | S1 | ACEITO | T2/T5; paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado no fluxo |
| `config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json` | S1 | ACEITO | T2/T5; paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado no fluxo |
| `config/telas/demo/h0045_paginacao_politicas_quebra.json` | S1 | ACEITO | T2/T5; paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; ID usado no fluxo |
| `config/telas/demo/h0045_validacao_continuacao.json` | S1 | ACEITO | T2/T5; casos de paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; caso resolvido para esqueleto |
| `config/telas/demo/h0045_validacao_fluxo_continuo.json` | S1 | ACEITO | T2/T5; casos de paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; caso resolvido para esqueleto |
| `config/telas/demo/h0045_validacao_manter_junto.json` | S1 | ACEITO | T2/T5; casos de paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; caso resolvido para esqueleto |
| `config/telas/demo/h0045_validacao_nova_pagina.json` | S1 | ACEITO | T2/T5; casos de paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; caso resolvido para esqueleto |
| `config/telas/demo/h0045_validacao_vazio.json` | S1 | ACEITO | T2/T5; casos de paginação | TELA_ESTRUTURAL | — | SIM | raiz estrutural; caso resolvido para esqueleto |
| `config/telas/demo/resultado_execucao.json` | S2 | ACEITO | T4; `carregar_sessao_resultado` e fluxo H-0043 | TELA_ESTRUTURAL | — | SIM | `perfil=resultado_execucao`; validação específica |
| `config/telas/demo/stub_b.json` | S0 | ACEITO | T1/T5; integração de composição/matriz | TELA_ESTRUTURAL | — | SIM | raiz estrutural; não é conteúdo |

Não há `ARTEFATO_AUXILIAR_NAO_TELA`: os oito D0 são consumidos como dados
externos. Não há `ARTEFATO_NAO_REFERENCIADO`: os nomes sem ocorrência literal
individual (`h0040_nav_console_nao_focalizavel`, `h0040_nav_degenere_uma_coluna`
e `h0040_nav_degenere_uma_linha`) são alcançados pelo resolvedor de caminho T3
e pelo loader T1. Não há `INCONCLUSIVO`.

## Consumidores dos dados externos

| Documento externo | Tela consumidora | Componente | Símbolo/mecanismo | Subtipo / apresentação | Referência de entrada |
|---|---|---|---|---|---|
| `h0035_console_com_conteudo.json` | `h0035_console_com` | `corpo.elementos[0]`, id `con` | `_CATALOGO_CONTEUDO_EXTERNO` → `carregar_conteudo_externo` → `construir_modelo` → `_linhas_console` | console / hierarquia | nome-base no catálogo |
| `h0035_console_sem_conteudo.json` | `h0035_console_sem` | `corpo.elementos[0]`, id `con` | mesmo fluxo | console / hierarquia | nome-base no catálogo |
| `h0036_conjuntos_conteudo.json` | `h0036_console_conjuntos` | `corpo.elementos[0]`, id `con` | mesmo fluxo | console / conjuntos_campos | nome-base no catálogo |
| `h0036_hierarquia_conteudo.json` | `h0036_console_hierarquia` | `corpo.elementos[0]`, id `con` | mesmo fluxo | console / hierarquia | nome-base no catálogo |
| `h0036_tabela_conteudo.json` | `h0036_console_tabela` | `corpo.elementos[0]`, id `con` | mesmo fluxo | console / tabela | nome-base no catálogo |
| `h0037_dois_niveis_conteudo.json` | `h0037_console_nao_verboso`; `h0037_console_verboso_dois_niveis` | `corpo.elementos[0]`, id `con`, em cada tela | mesmo fluxo; fonte compartilhada | console / hierarquia | duas entradas apontam ao mesmo nome-base |
| `h0037_tabela_conteudo.json` | `h0037_console_tabela_alternavel` | `corpo.elementos[0]`, id `con` | mesmo fluxo | console / tabela | nome-base no catálogo |
| `h0037_tres_niveis_conteudo.json` | `h0037_console_alternavel_tres_niveis` | `corpo.elementos[0]`, id `con` | mesmo fluxo | console / hierarquia | nome-base no catálogo |

O conteúdo não é inserido na raiz estrutural: `construir_modelo` o mantém em
`ModeloTela.conteudo_externo` e o propaga ao console. Portanto, `cabecalho`
eventual em dados de componente seria conteúdo exibido, não o cabeçalho
estrutural; nos oito D0 auditados não há campo raiz `cabecalho`.

## Manifesto candidato de migração

São exatamente os 72 arquivos classificados como `TELA_ESTRUTURAL` na matriz:

```text
config/telas/demo/demo.json
config/telas/demo/destino_minimo.json
config/telas/demo/grupo_minimo.json
config/telas/demo/h0029_dashboard_fracao.json
config/telas/demo/h0029_dashboard_igual.json
config/telas/demo/h0029_dashboard_percentual.json
config/telas/demo/h0029_grupo_fracao.json
config/telas/demo/h0029_grupo_igual.json
config/telas/demo/h0029_grupo_pai_distribuido.json
config/telas/demo/h0029_grupo_percentual.json
config/telas/demo/h0030_console_unico.json
config/telas/demo/h0030_dashboard_unico.json
config/telas/demo/h0030_matriz_2x2.json
config/telas/demo/h0030_matriz_2x4.json
config/telas/demo/h0030_matriz_3x2.json
config/telas/demo/h0035_catalogo.json
config/telas/demo/h0035_centralizado_h_colunas.json
config/telas/demo/h0035_console_com.json
config/telas/demo/h0035_console_sem.json
config/telas/demo/h0035_dashboard_com.json
config/telas/demo/h0035_dashboard_sem.json
config/telas/demo/h0035_esquerda_margens_min_max.json
config/telas/demo/h0035_h_margens_limitadas.json
config/telas/demo/h0035_h_uniforme.json
config/telas/demo/h0035_lancador_com.json
config/telas/demo/h0035_lancador_sem.json
config/telas/demo/h0035_matriz_fixa_cabe.json
config/telas/demo/h0035_matriz_fixa_quadro_minimo.json
config/telas/demo/h0035_minimo_fixo_excedido.json
config/telas/demo/h0035_pref_colunas.json
config/telas/demo/h0035_pref_linhas.json
config/telas/demo/h0035_quatro_centralizados.json
config/telas/demo/h0035_resto_horizontal.json
config/telas/demo/h0035_resto_vertical.json
config/telas/demo/h0035_tres_centralizados.json
config/telas/demo/h0035_um_centralizado.json
config/telas/demo/h0035_uma_coluna.json
config/telas/demo/h0035_uma_linha.json
config/telas/demo/h0035_v_margens_min.json
config/telas/demo/h0035_v_margens_min_max.json
config/telas/demo/h0035_v_uniforme.json
config/telas/demo/h0036_console_conjuntos.json
config/telas/demo/h0036_console_hierarquia.json
config/telas/demo/h0036_console_tabela.json
config/telas/demo/h0037_console_alternavel_tres_niveis.json
config/telas/demo/h0037_console_nao_verboso.json
config/telas/demo/h0037_console_tabela_alternavel.json
config/telas/demo/h0037_console_verboso_dois_niveis.json
config/telas/demo/h0040_nav_console_grade_2x3.json
config/telas/demo/h0040_nav_console_nao_focalizavel.json
config/telas/demo/h0040_nav_console_unico_linear.json
config/telas/demo/h0040_nav_degenere_um_item.json
config/telas/demo/h0040_nav_degenere_uma_coluna.json
config/telas/demo/h0040_nav_degenere_uma_linha.json
config/telas/demo/h0040_nav_dois_consoles.json
config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
config/telas/demo/h0041_selecao_multipla_oito_itens.json
config/telas/demo/h0044_fluxo_execucao_integrado.json
config/telas/demo/h0045_dois_consoles_paginas_independentes.json
config/telas/demo/h0045_fluxo_execucao_paginado.json
config/telas/demo/h0045_paginacao_conjunto_vazio.json
config/telas/demo/h0045_paginacao_console_unico.json
config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
config/telas/demo/h0045_paginacao_politicas_quebra.json
config/telas/demo/h0045_validacao_continuacao.json
config/telas/demo/h0045_validacao_fluxo_continuo.json
config/telas/demo/h0045_validacao_manter_junto.json
config/telas/demo/h0045_validacao_nova_pagina.json
config/telas/demo/h0045_validacao_vazio.json
config/telas/demo/resultado_execucao.json
config/telas/demo/stub_b.json
```

## Manifesto de preservação e hashes SHA-256

Os oito arquivos abaixo devem permanecer integralmente fora da migração de
`cabecalho.apresentacao`:

```text
1ec153da3e18830562c8c695f83b45a79143e9a9600f54864fde295071b8e71e  config/telas/demo/h0035_console_com_conteudo.json
fa684bfabd2d76a2eccc5b1abd1f408378542db070012e9ce88787c22dba0337  config/telas/demo/h0035_console_sem_conteudo.json
1a3a9a1e9c1addd316feb1bebca6c79148efc10de02b7a9f4207b6924f731dcc  config/telas/demo/h0036_conjuntos_conteudo.json
e25774c1f92e55b8d8ffa39fe03c1534d1ec7d36989e1146ea5fc4dbd3cca3ac  config/telas/demo/h0036_hierarquia_conteudo.json
eacd1e366526dae88fbc64d52f28f39186d9ec2147cf82d5dcb3c059c3df4dd5  config/telas/demo/h0036_tabela_conteudo.json
0463452913a87c715163778dab539d5b6a16e65e81cb7e6589b3b3b76672a317  config/telas/demo/h0037_dois_niveis_conteudo.json
60042955a4651c19ad7081e3b8e88a693bc820db37d444e8fc7a210f04fa6fcc  config/telas/demo/h0037_tabela_conteudo.json
887fde5901ec198831e6aa505ad7e3af6b815731d1ca0dbbb3ab35f1c9d719b1  config/telas/demo/h0037_tres_niveis_conteudo.json
```

`config/elementos/cabecalho.json` está fora de `config/telas` e não integra o
inventário. A auditoria não o altera; sua situação posterior deve continuar
sendo tratada pelo próprio H-0049, sem confundi-lo com dados externos de
componente.

## Revisão factual do H-0049 e dos QAs

1. O total correto de JSONs sob `config/telas` é 80. O alvo de migração é 72,
   não 74. A contagem 72 anterior coincide apenas com a quantidade estrutural
   descoberta agora; não é uma contagem exaustiva do diretório.
2. O manifesto de 74 do H-0049 contém indevidamente
   `h0036_tabela_conteudo.json` e `h0037_tabela_conteudo.json`. Eles devem ser
   removidos do manifesto candidato.
3. Os seis outros documentos externos também não são telas e devem ser
   preservados: `h0035_console_com_conteudo`, `h0035_console_sem_conteudo`,
   `h0036_conjuntos_conteudo`, `h0036_hierarquia_conteudo`,
   `h0037_dois_niveis_conteudo` e `h0037_tres_niveis_conteudo`.
4. A afirmação de que todos os 74 JSONs nominais são entradas reais do loader
   estrutural é falsa. O teste nominal deve carregar 72 com `carregar_tela` e
   verificar separadamente os oito com `carregar_conteudo_externo`.
5. O aceite “migrar 74 JSONs” e a saída de implementação que registra 74
   precisam ser corrigidos para 72; a lista de preservação precisa incluir os
   oito dados externos e seus hashes.
6. Os dois QAs corretamente identificaram `resultado_execucao.json` e
   `stub_b.json` como telas que completam a lista estrutural, mas a explicação
   da divergência deve ser limitada à contagem histórica anterior; eles já
   estão no manifesto atual e não são adições pendentes.
7. Critérios baseados em ocorrência de `cabecalho`, nome do arquivo ou
   proximidade falham: o contrato do conteúdo externo é D0 e o consumidor
   real é determinado pelo catálogo + loader próprio + console. As buscas
   textuais anteriores não distinguem esses fluxos.

Não houve arquivo inconclusivo, dependência externa necessária para decidir a
classificação, JSON inválido, duplicidade de caminho ou diferença entre a soma
das categorias e o `find`: `72 + 8 + 0 + 0 + 0 = 80`. Nenhum patch do H-0049,
JSON, código, teste, stage ou commit foi produzido nesta auditoria.

```yaml
consistencia:
  total_inventariado: 80
  soma_das_classificacoes: 80
  caminhos_duplicados: 0
  caminhos_sem_classificacao: 0
  arquivos_inexistentes: 0
  jsons_invalidos: 0
```
