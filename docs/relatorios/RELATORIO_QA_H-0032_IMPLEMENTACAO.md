# RELATORIO_QA_H-0032_IMPLEMENTACAO

## 1. Identificacao

```yaml
etapa: QA_IMPLEMENTACAO
handoff: docs/handoff/H-0032-migracao-estrutural-demonstracao-configuracoes.md
relatorio: docs/relatorios/RELATORIO_QA_H-0032_IMPLEMENTACAO.md
data: 2026-07-15
auditor: Codex
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: I2_IMPLEMENTATION_PATCH_REQUIRED
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 2. Objetivo e limites

Auditoria independente da implementacao do H-0032. Nao foram feitas correcoes
na implementacao, no handoff ou no relatorio de implementacao; nao houve stage,
commit, stash ou movimentacao de arquivos. O unico arquivo criado nesta etapa
foi este relatorio.

Antes da criacao deste arquivo foi executado:

```bash
test ! -e docs/relatorios/RELATORIO_QA_H-0032_IMPLEMENTACAO.md
```

Resultado: codigo de saida `0`.

## 3. Estado Git inicial

Comandos executados da raiz:

```yaml
git_rev_parse_show_toplevel: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
pwd: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
head_abreviado: 0143fd1
ultimo_commit: "0143fd1 chore: migra orquestrador para repositorio independente"
git_diff_check: sem_erros
git_diff_cached_name_only: vazio
git_stash_list: vazio
stage: vazio
commit_novo: nenhum
```

`git status --short` iniciou com alteracoes rastreadas e nao rastreadas. Para
itens documentais acumulados e caches ja presentes:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

## 4. Autoridades

Lidos integralmente:

```text
docs/handoff/H-0032-migracao-estrutural-demonstracao-configuracoes.md
docs/relatorios/RELATORIO_QA_H-0032_HANDOFF.md
docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
```

Consultados conforme necessidade:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0022.md
```

Confirmacao do QA do handoff:

```text
status_literal: H1_HANDOFF_APPROVED
```

Contratos ativos citados pelo handoff foram considerados como autoridade de
semantica e escopo; a auditoria concentrou a verificacao fisica nos arquivos
realmente afetados pelo H-0032.

## 5. Artefatos auditados

```text
tela/loader.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
demo/demo.py
demo/diagnostico.py
demo/explorar_barra_de_menus.py
demo/teste_demo.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
config/telas/demo/*.json
config/layouts/*.json
config/elementos/*.json
config/estilo.json
docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md
```

## 6. Isolamento do delta

Arquivos removidos dos caminhos antigos:

```text
tela/demo.py
tela/diagnostico.py
tela/explorar_barra_de_menus.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
config/telas/destino_minimo.json
config/telas/grupo_minimo.json
config/telas/h0029_dashboard_fracao.json
config/telas/h0029_dashboard_igual.json
config/telas/h0029_dashboard_percentual.json
config/telas/h0029_grupo_fracao.json
config/telas/h0029_grupo_igual.json
config/telas/h0029_grupo_pai_distribuido.json
config/telas/h0029_grupo_percentual.json
config/telas/h0030_console_unico.json
config/telas/h0030_dashboard_unico.json
config/telas/h0030_matriz_2x2.json
config/telas/h0030_matriz_2x4.json
config/telas/h0030_matriz_3x2.json
config/telas/orquestrador.json
config/telas/stub_b.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json
config/cabecalho.json
config/barra_de_menus.json
config/lancador.json
```

Arquivos criados nos caminhos novos:

```text
demo/demo.py
demo/diagnostico.py
demo/explorar_barra_de_menus.py
demo/teste_demo.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
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
config/telas/demo/stub_b.json
config/layouts/layout_console.json
config/layouts/layout_dado.json
config/layouts/layout_menu.json
config/elementos/cabecalho.json
config/elementos/barra_de_menus.json
config/elementos/lancador.json
```

Arquivos modificados:

```text
tela/loader.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Arquivos preservados:

```text
tela/modelo.py
tela/renderizador.py
tela/__init__.py
config/estilo.json
```

Arquivos inesperados observados no workspace:

```yaml
tela/__pycache__/teste_loader.cpython-314.pyc:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
tela/__pycache__/teste_renderizador.cpython-314.pyc:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
documentos ADR/relatorios nao rastreados e diffs documentais acumulados:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
```

## 7. Estrutura final

Confirmados:

```text
demo/
config/telas/demo/
config/layouts/
config/elementos/
```

Confirmadas ausencias:

```text
orquestrador.py
demo/__init__.py
config/telas/orquestrador.json
config/telas/demo/orquestrador.json
```

Nenhuma tela demonstrativa permanece diretamente em `config/telas/`.

## 8. Diretorios criados

```yaml
demo/: conforme
config/telas/demo/: conforme
config/layouts/: conforme
config/elementos/: conforme
```

## 9. Scripts e testes movidos

Os seis arquivos antigos foram removidos e os seis destinos existem. Nao foram
encontradas copias, wrappers ou aliases nos caminhos antigos.

Comparacao com `HEAD`:

```yaml
tela/demo.py -> demo/demo.py:
  derivado: sim
  ratio_difflib: 0.9772
  deltas: docstring/comando, _RAIZ_TELAS_DEMO, tela_atual demo, raiz_telas
tela/diagnostico.py -> demo/diagnostico.py:
  derivado: sim
  ratio_difflib: 0.7229
  deltas: docstring, import os, _RAIZ_TELAS_DEMO, padrao demo, raiz_telas
tela/explorar_barra_de_menus.py -> demo/explorar_barra_de_menus.py:
  derivado: sim
  ratio_difflib: 0.9972
  deltas: comandos documentados
tela/teste_demo.py -> demo/teste_demo.py:
  derivado: sim
  ratio_difflib: 0.9458
  deltas: imports demo.*, subprocessos, raiz demo, remocao de demo/ em sys.path
tela/teste_diagnostico.py -> demo/teste_diagnostico.py:
  derivado: sim
  ratio_difflib: 0.9096
  deltas: imports demo.*, bootstrap, padrao demo, raiz demo
tela/teste_explorar_barra_de_menus.py -> demo/teste_explorar_barra_de_menus.py:
  derivado: sim
  ratio_difflib: 0.9877
  deltas: _SCRIPT para demo/, imports demo.*, bootstrap
```

## 10. Imports

```yaml
demo/demo.py:
  bootstrap_encontrado: sim
  calculo_da_raiz: string sobre __file__ removendo dois componentes finais
  usa___file__: sim
  altera_sys_path: sim, somente quando __main__
  remove_demo_do_sys_path: nao aplicavel
  depende_de_cwd: nao para imports; comandos auditados partem da raiz
  usa_PYTHONPATH: nao
  resultado: conforme_com_observacao_textual

demo/diagnostico.py:
  bootstrap_encontrado: sim
  calculo_da_raiz: string sobre __file__ removendo dois componentes finais
  usa___file__: sim
  altera_sys_path: sim, somente quando __main__
  remove_demo_do_sys_path: nao aplicavel
  depende_de_cwd: nao para imports
  usa_PYTHONPATH: nao
  resultado: conforme

demo/explorar_barra_de_menus.py:
  bootstrap_encontrado: sim
  calculo_da_raiz: Path(__file__).resolve().parent.parent
  usa___file__: sim
  altera_sys_path: sim
  remove_demo_do_sys_path: nao
  depende_de_cwd: nao para imports
  usa_PYTHONPATH: nao
  resultado: conforme

demo/teste_demo.py:
  bootstrap_encontrado: sim
  calculo_da_raiz: Path(__file__).resolve().parent.parent
  usa___file__: sim
  altera_sys_path: sim
  remove_demo_do_sys_path: sim
  depende_de_cwd: comandos auditados partem da raiz
  usa_PYTHONPATH: nao
  resultado: conforme_com_observacao_textual

demo/teste_diagnostico.py:
  bootstrap_encontrado: sim
  calculo_da_raiz: Path(__file__).resolve().parent.parent
  usa___file__: sim
  altera_sys_path: sim
  remove_demo_do_sys_path: sim
  depende_de_cwd: comandos auditados partem da raiz
  usa_PYTHONPATH: nao
  resultado: conforme

demo/teste_explorar_barra_de_menus.py:
  bootstrap_encontrado: sim
  calculo_da_raiz: Path(__file__).resolve().parent.parent
  usa___file__: sim
  altera_sys_path: sim
  remove_demo_do_sys_path: sim
  depende_de_cwd: comandos auditados partem da raiz
  usa_PYTHONPATH: nao
  resultado: conforme
```

`import demo.demo` foi validado sem `demo/__init__.py`, com namespace package.
Nao foi encontrado fallback de importacao que oculte erro.

## 11. Motor compartilhado

`git diff -- tela/loader.py` mostra apenas a mudanca de assinatura e resolucao
de caminho:

```yaml
carregar_tela:
  assinatura: carregar_tela(caminho_base, id_tela, raiz_telas=None)
  default: config/telas
  raiz_demo: deve ser passada explicitamente
  fallback_entre_raizes: ausente
  validacao_id_basename: preservada
```

`git diff --exit-code -- tela/modelo.py` retornou `0`.
`git diff --exit-code -- tela/renderizador.py` retornou `0`.

## 12. Testes compartilhados

Alteracoes auditadas:

```yaml
tela/teste_loader.py:
  alteracoes: _RAIZ_TELAS_DEMO, chamadas com raiz demo, novo teste teste_raiz_telas_h0032
  novos_testes_materiais:
    - carregar_tela(demo, raiz_demo) carrega sem excecao
    - id carregado e demo
    - carregar_tela(demo) sem raiz levanta TelaArquivoNaoEncontrado
    - carregar_tela(orquestrador) sem raiz levanta TelaArquivoNaoEncontrado
    - TelaIdNaoCoincideComArquivo funciona com raiz_telas explicita
  resultado: conforme

tela/teste_modelo.py:
  alteracoes: chamadas demonstrativas passam raiz demo; identidade esperada demo
  resultado: conforme

tela/teste_renderizador.py:
  alteracoes: chamadas demonstrativas passam raiz demo; snapshots preservam titulo visual ORQUESTRADOR
  resultado: conforme_com_residuos_textuais_baixos
```

Nao foi identificada reducao de testes nem alteracao funcional de expectativas
para ocultar regressao.

## 13. Telas demonstrativas

Todos os arquivos nominais existem em `config/telas/demo/`:

```text
demo.json
destino_minimo.json
grupo_minimo.json
h0029_dashboard_fracao.json
h0029_dashboard_igual.json
h0029_dashboard_percentual.json
h0029_grupo_fracao.json
h0029_grupo_igual.json
h0029_grupo_pai_distribuido.json
h0029_grupo_percentual.json
h0030_console_unico.json
h0030_dashboard_unico.json
h0030_matriz_2x2.json
h0030_matriz_2x4.json
h0030_matriz_3x2.json
stub_b.json
```

Comparacao byte a byte com `HEAD` para os 15 arquivos movidos sem renomeacao:

```text
IDENTICO
```

## 14. demo.json

Comparacao estrutural independente:

```yaml
HEAD:config/telas/orquestrador.json:
  id: orquestrador
config/telas/demo/demo.json:
  id: demo
demais_campos:
  resultado: IDENTICO
```

Conforme: a unica diferenca estrutural e o campo `id`.

## 15. Configuracoes gerais

Movimentacoes confirmadas e conteudo byte a byte identico ao `HEAD`:

```text
config/layout_console.json -> config/layouts/layout_console.json
config/layout_dado.json -> config/layouts/layout_dado.json
config/layout_menu.json -> config/layouts/layout_menu.json
config/cabecalho.json -> config/elementos/cabecalho.json
config/barra_de_menus.json -> config/elementos/barra_de_menus.json
config/lancador.json -> config/elementos/lancador.json
```

As ocorrencias internas antigas nesses JSONs foram preservadas por serem parte
do conteudo movido sem alteracao, conforme a autorizacao de preservacao de
valores.

## 16. Preservacao de estilo

```yaml
git_diff_exit_code_config_estilo: 0
find_config_estilo: config/estilo.json
resultado: conforme
```

Nao ha copia de estilo em outro diretorio.

## 17. Selecao explicita da raiz

Evidencia operacional:

```yaml
identidade_carregada: demo
raiz_de_telas: config/telas/demo
motor_compartilhado_loader: tela.loader
motor_compartilhado_demo_loader: tela.loader
sem_fallback_demo: "Arquivo nao encontrado: config/telas/demo.json"
sem_fallback_orquestrador: "Arquivo nao encontrado: config/telas/orquestrador.json"
demo_init_existe: false
config_telas_orquestrador_existe: false
demo_py_namespace_import: demo.demo
```

Nao foi encontrada busca automatica nas duas raizes, alias
`orquestrador -> demo`, duplicacao da tela raiz ou fallback silencioso.

## 18. Referencias antigas

A busca obrigatoria encontrou muitas ocorrencias historicas em handoffs,
relatorios e ADRs antigas. Essas foram classificadas como historico preservado,
relatorio, handoff encerrado ou reserva documental do produto real.

Ocorrencias relevantes em arquivos ativos:

```yaml
demo/demo.py:
  linhas_textuais:
    - docstring ainda cita default "orquestrador"
    - docstring ainda cita carregar_tela(None, tela_atual) sem raiz
  classificacao: observacao_baixa

demo/teste_demo.py:
  linhas_textuais:
    - "config/telas/demo.json inalterado apos demo"
  classificacao: observacao_baixa

tela/teste_loader.py:
  linhas_textuais:
    - comentario "orquestrador real declara distribuicao"
  classificacao: observacao_baixa

tela/teste_renderizador.py:
  linhas_textuais:
    - comentarios sobre "orquestrador real" e "orquestrador.json real"
    - prints ainda dizem config/telas/destino_minimo.json e grupo_minimo.json
  classificacao: observacao_baixa
```

Nao foram encontradas referencias operacionais residuais que executem arquivos
antigos como `tela/demo.py` ou carreguem `config/telas/orquestrador.json`.

## 19. Arquivos fora da lista

```yaml
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md:
  origem: NAO_CONFIRMADA
  necessidade: autoridade preexistente do ciclo
  autorizacao_explicita: nao aplicavel nesta auditoria
  aderencia: fora_do_delta_da_implementacao_auditado

docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md:
  origem: NAO_CONFIRMADA
  necessidade: autoridade preexistente do ciclo
  autorizacao_explicita: nao aplicavel nesta auditoria
  aderencia: fora_do_delta_da_implementacao_auditado

docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md:
  origem: executor H-0032
  necessidade: relatorio obrigatorio do handoff
  autorizacao_explicita: sim, handoff secao 25
  aderencia: nao_conforme, ver achado ACH-H0032-001
```

## 20. Fidelidade do relatorio de implementacao

O relatorio `IMP-0032` registra parte da implementacao e as contagens da suite,
mas nao atende integralmente a lista obrigatoria do handoff.

Itens ausentes ou insuficientes:

```yaml
estado_git_inicial: ausente
workspace_documental_preexistente: ausente
linha_de_base_anterior: incompleta
estrutura_anterior: ausente
diretorios_criados: incompleto, nao registra config/layouts e config/elementos
arquivos_movidos: incompleto, nao lista nominalmente as 21 telas/configuracoes movidas
arquivos_renomeados: parcial
arquivos_preservados: incompleto
referencias_historicas_preservadas: ausente
seis_contagens_antes_e_depois: incompleto, registra minimo e final mas nao baseline individual completa antes/depois
codigos_de_saida: ausentes na tabela
demonstracao_operacional: insuficiente como prova semantica isolada
fatos_NAO_CONFIRMADOS: ausentes
arquivos_inesperados: ausentes
estado_git_final: incompleto
conclusao_factual: parcial
```

Conclusao: a implementacao fisica principal esta tecnicamente conforme, mas o
relatorio de implementacao obrigatorio precisa de patch local.

## 21. Reproducao da suite

Comandos executados da raiz com bytecode desabilitado para nao criar caches
durante a auditoria:

```yaml
- script: tela/teste_loader.py
  comando: python -B tela/teste_loader.py
  aprovados: 249
  total: 249
  codigo_saida: 0
  baseline_minima: 244
  diferenca: +5
  resultado: PASSOU

- script: tela/teste_modelo.py
  comando: python -B tela/teste_modelo.py
  aprovados: 148
  total: 148
  codigo_saida: 0
  baseline_minima: 148
  diferenca: 0
  resultado: PASSOU

- script: tela/teste_renderizador.py
  comando: python -B tela/teste_renderizador.py
  aprovados: 980
  total: 980
  codigo_saida: 0
  baseline_minima: 980
  diferenca: 0
  resultado: PASSOU

- script: demo/teste_demo.py
  comando: python -B demo/teste_demo.py
  aprovados: 358
  total: 358
  codigo_saida: 0
  baseline_minima: 358
  diferenca: 0
  resultado: PASSOU

- script: demo/teste_diagnostico.py
  comando: python -B demo/teste_diagnostico.py
  aprovados: 30
  total: 30
  codigo_saida: 0
  baseline_minima: 28
  diferenca: +2
  resultado: PASSOU

- script: demo/teste_explorar_barra_de_menus.py
  comando: python -B demo/teste_explorar_barra_de_menus.py
  aprovados: 38
  total: 38
  codigo_saida: 0
  baseline_minima: 38
  diferenca: 0
  resultado: PASSOU
```

```yaml
suite_baseline: 1796/1796
suite_reproduzida: 1803/1803
git_diff_check: sem_erros
```

As contagens reais coincidem com o declarado pelo executor.

## 22. Independencia dos testes

Os testes novos do loader usam constantes independentes:

```yaml
id_esperado: demo
raiz_esperada: config/telas/demo
ausencia_de_fallback:
  - carregar_tela(_BASE_PADRAO, "demo") deve falhar em config/telas/demo.json
  - carregar_tela(_BASE_PADRAO, "orquestrador") deve falhar em config/telas/orquestrador.json
```

O esperado nao e derivado da propria funcao auditada. A validacao de id divergente
usa fixture temporaria com `id: outro_id`, suficiente para preservar a regra
basename/id.

## 23. Demonstracao operacional

Comando localizado no handoff e no relatorio de implementacao:

```bash
python demo/diagnostico.py
```

Executado como:

```bash
python -B demo/diagnostico.py
```

Saida relevante:

```text
╭ ORQUESTRADOR ──────────────────────────╮
│ Tela raiz do sistema — ponto de entrada│
...
│ [d] Destino                            │
│ [g] Grupo Min.                         │
│ [1] Console                            │
...
│  [Esc] Sair  [?] Ajuda                 │
```

A saida visual isolada nao expõe semanticamente `id=demo` nem a raiz usada.
Por isso foi executada prova complementar independente:

```yaml
script_executado: demo/diagnostico.py e snippet de verificacao semantica
identidade_observada: demo
raiz_observada: config/telas/demo
motor_compartilhado: tela.loader
alias_orquestrador: ausente
fallback_para_config_telas: ausente
mecanismo_de_comprovacao: carregar_tela(None, "demo") e carregar_tela(None, "orquestrador") falham na raiz produto
validacao_operacional: CONFORME_COM_OBSERVACAO_SOBRE_RELATORIO_IMP
```

## 24. Validacao manual

```yaml
validacao_manual: NAO_APLICAVEL
justificativa: migracao estrutural; criterios comprovados automaticamente; sem alteracao intencional de renderizacao, interacao, redraw, cursor, echo ou resize
```

## 25. Escopo negativo

Confirmada ausencia de:

```text
orquestrador.py
config/telas/orquestrador.json como tela real
config/telas/demo/orquestrador.json
demo/__init__.py
titulo e descricao da tela real
barra real com Estilos
acao ou destino de Estilos
tela funcional de estilos
integracao com Pipeline
mudanca de schema
novo tipo de elemento
mudanca funcional de layout
correcao de destino_minimo
correcao de grupo_minimo
alteracao demonstrativa alem do id de demo.json
```

`destino_minimo.json` e `grupo_minimo.json` foram comparados com `HEAD` e estao
identicos, apenas movidos.

## 26. Achados

```yaml
- id: ACH-H0032-001
  severidade: medio
  titulo: Relatorio de implementacao obrigatorio esta incompleto
  arquivo: docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md
  secao_ou_trecho: documento inteiro, especialmente secoes 2, 3 e 5
  evidencia: nao registra estado Git inicial, workspace preexistente, estrutura anterior, lista nominal completa de configuracoes movidas, codigos de saida, fatos NAO_CONFIRMADOS, arquivos inesperados e estado Git final completo; a demonstracao operacional exibida nao prova sozinha id/raiz/fallback
  autoridade_afetada: H-0032 secao 25 e prompt de QA_IMPLEMENTACAO
  impacto: impede aprovacao formal I1, embora a implementacao fisica principal esteja conforme
  correcao_necessaria: patch do relatorio de implementacao para registrar as evidencias obrigatorias e reconciliar listas/numeros com o estado real

- id: ACH-H0032-002
  severidade: baixo
  titulo: Residuos textuais ativos mencionam caminhos ou identidade antigos
  arquivo: demo/demo.py; demo/teste_demo.py; tela/teste_loader.py; tela/teste_renderizador.py
  secao_ou_trecho: docstrings, comentarios e mensagens de teste
  evidencia: demo/demo.py ainda documenta tela_atual default "orquestrador" e carregar_tela(None, tela_atual); demo/teste_demo.py cita config/telas/demo.json; testes compartilhados ainda comentam "orquestrador real" e prints com config/telas/destino_minimo.json
  autoridade_afetada: H-0032 secoes 17, 18 e 20
  impacto: nao afeta execucao nem prova de raiz, mas reduz clareza operacional em arquivos ativos
  correcao_necessaria: atualizar textos ativos para refletir demo e config/telas/demo/ sem alterar semantica
```

## 27. Estado Git final

Comandos finais previstos/executados ao encerrar:

```yaml
git_diff_check: sem_erros
git_diff_cached_name_only: vazio
git_log_1_oneline: "0143fd1 chore: migra orquestrador para repositorio independente"
git_stash_list: vazio
stage: vazio
commit_novo: nenhum
caches_observados: somente tela/__pycache__ preexistente de origem NAO_CONFIRMADA
temporarios_h0032_em_tmp: ausentes
arquivo_criado_pelo_auditor:
  - docs/relatorios/RELATORIO_QA_H-0032_IMPLEMENTACAO.md
```

## 28. Status final

```text
I2_IMPLEMENTATION_PATCH_REQUIRED
```

Justificativa: a implementacao fisica principal, as movimentacoes, a suite, a
raiz explicita, a ausencia de fallback e o escopo negativo estao conformes. A
aprovacao I1 fica impedida porque o relatorio de implementacao obrigatorio nao
cumpre a completude exigida pelo handoff, e porque ha residuos textuais ativos
de baixo impacto que devem ser limpos em patch de implementacao/documentacao
local.

## 29. Proxima categoria

```text
PATCH_IMPLEMENTACAO
```

## Saida padrao

```text
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: I2_IMPLEMENTATION_PATCH_REQUIRED
relatorio: docs/relatorios/RELATORIO_QA_H-0032_IMPLEMENTACAO.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 1
achados_baixos: 1
observacoes: 0
arquivos_movidos_auditados: 27
arquivos_renomeados_auditados: 1
arquivos_modificados_auditados: 4
diretorios_criados_auditados: 4
suite_baseline: 1796/1796
suite_reproduzida: 1803/1803
validacao_operacional: CONFORME_COM_OBSERVACAO_SOBRE_RELATORIO_IMP
validacao_manual: NAO_APLICAVEL
escopo_negativo: CONFORME
estado_git: stage_vazio_sem_commit_sem_stash_com_relatorio_QA_criado
proxima_categoria: PATCH_IMPLEMENTACAO
```
