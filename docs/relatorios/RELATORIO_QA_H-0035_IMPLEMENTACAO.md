---
id: RELATORIO_QA_H-0035_IMPLEMENTACAO
tipo: qa_implementacao
handoff: H-0035
data: 2026-07-16
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: IMPLEMENTATION_PATCH_REQUIRED
---

# RELATORIO QA H-0035 IMPLEMENTACAO

## 1. Identificacao

Auditoria independente da implementacao do H-0035 -- Distribuicao matricial
configuravel de nivel unico do conteudo dos elementos.

Relatorio criado nesta etapa:

```text
docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
```

## 2. Objetivo

Auditar a implementacao contra o handoff aprovado, ADR-0025 aplicada,
contratos ativos, relatorio de implementacao, estado Git real, arquivos
criados/alterados, testes automatizados, demo dedicado, fallback, recuperacao e
validacao manual pendente.

Este QA nao corrigiu codigo, testes, JSONs, demos, contratos, ADRs, handoff ou
relatorio de implementacao.

## 3. Handoff e QAs

Handoff auditado:

```text
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

QAs lidos:

```text
docs/relatorios/RELATORIO_QA_H-0035_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_HANDOFF.md
```

Status final do QA de handoff:

```yaml
status_literal: H1_HANDOFF_APPROVED
status_normalizado: HANDOFF_APPROVED
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
decisoes_ausentes: 0
contradicoes_documentais: 0
proxima_categoria: IMPLEMENTAR
```

## 4. Relatorio de implementacao

Relatorio auditado:

```text
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Declarou implementacao, 26 caminhos validados, 28 familias cobertas, testes
passando e validacao manual TTY pendente do usuario.

## 5. Autoridades

Autoridades lidas e usadas como criterio:

```text
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_QA_H-0035_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_HANDOFF.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
docs/adr/ADR-0001-menu-suporta-matriz.md
docs/adr/ADR-0002-menu-sobra-direita.md
docs/adr/ADR-0003-vaos-elasticos-menu.md
docs/adr/ADR-0023-largura-minima-funcional-lancador.md
```

## 6. Estado Git inicial

Comandos executados antes da criacao deste relatorio:

```text
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff --cached --name-only
```

Resultado material:

```yaml
arquivos_rastreados_modificados:
  implementacao_codigo_teste:
    - demo/teste_diagnostico.py
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
  documentais_preexistentes:
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_json_dashboard.md
    - docs/contratos/contrato_json_lancador.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_tela_json.md
stage: vazio
git_diff_check: sem_saida_material
```

Arquivos nao rastreados iniciais: 40. Destes, 31 pertencem materialmente a
lista autorizada de criacao da implementacao; 9 sao documentos do ciclo
ADR/handoff preexistente e nao foram atribuidos ao executor deste QA.

## 7. Diff real

`git diff --stat` registrou 15 arquivos rastreados modificados e 1965
insercoes / 3 delecoes. `git diff --name-only` lista apenas rastreados, portanto
nao cobre os 31 novos arquivos autorizados.

```yaml
diff_rastreado:
  arquivos: 15
  insercoes: 1965
  delecoes: 3
nao_rastreados_total: 40
stage: vazio
```

## 8. Lista nominal

Classificacao:

```yaml
arquivos_existentes_autorizados:
  esperados: 7
  alterados:
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
    - demo/teste_diagnostico.py
novos_arquivos_unicos_autorizados:
  esperados: 31
  criados: 31
configuracoes_json:
  esperadas: 26
  criadas: 26
relatorio_implementacao:
  esperado: 1
  criado: 1
preexistente_preservado:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_dashboard.md
  - docs/contratos/contrato_json_lancador.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
origem_nao_confirmada:
  - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  - docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_H-0035_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_HANDOFF.md
```

Para todos os itens de `origem_nao_confirmada`:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

## 9. Resolucao de 31 versus 32

```yaml
arquivos_criados_listados_no_retorno: 31
arquivos_criados_reais: 31
arquivo_adicional_se_existir: nenhum
classificacao_do_arquivo_adicional: nao_aplicavel
impacto: erro apenas do resumo que declarou 32 criados
```

O Git real nao confirma arquivo adicional autorizado ou nao autorizado da
implementacao H-0035. A divergencia vem da contagem do retorno, nao de arquivo
extra detectado.

## 10. Fidelidade do relatorio

Pontos fieis:

- lista nominal de arquivos alterados em `docs/relatorios/IMP-0035-...md` e
  arquivos reais do §22 coincidem;
- lista de criados do relatorio equivale a 31 arquivos reais: 4 codigo/demo/
  teste, 26 JSONs e 1 relatorio;
- testes declarados foram reexecutados com saida verde;
- validacao manual foi corretamente declarada como pendente;
- nao houve autoaprovacao.

Divergencias:

- o retorno externo declarou "32 criados", mas o Git confirma 31 arquivos de
  implementacao;
- o relatorio declara cumprimento de `minimo_fixo` sem desvio; entretanto o
  renderer introduz corte visual do conteudo do participante sob `minimo_fixo`,
  violando H-0035 §17 e contrato_json_dashboard.md §9.2.1.

## 11. 26 caminhos

```yaml
quantidade_esperada: 26
quantidade_implementada: 26
quantidade_validada: 26
faltantes: []
adicionais: []
literais_divergentes: []
tipos_divergentes: []
dependencias_ausentes: []
restricoes_cruzadas_ausentes: []
```

O loader valida os caminhos de `formacao.politica` a
`alinhamento_interno.vertical`, incluindo vocabulario fechado, minimo, maximo,
dependencias de `matriz_fixa`, dependencias de `minimo_fixo`, campos
desconhecidos e ausencia de defaults estruturais. Console e lancador remetem ao
mesmo vocabulario do dashboard.

## 12. Loader

Auditoria:

```yaml
estrutura_valida_completa: coberta
estrutura_valida_minima: coberta
ausencia_do_campo: aceita_sem_default
campo_desconhecido: rejeitado
tipo_incorreto: rejeitado
literal_invalido: rejeitado
valor_negativo: rejeitado
maximo_inferior_ao_minimo: rejeitado
matriz_fixa_incompleta: rejeitada
dependencia_ausente: rejeitada
combinacao_contraditoria: rejeitada
linhas_colunas_invalidas: rejeitadas
classe_de_erro: TelaEstruturaInvalida
mensagem_material: presente
efeito_parcial: nao_observado
```

A validacao ocorre em `carregar_tela` antes de construcao de modelo e antes de
renderizacao.

## 13. Modelo

`ElementoCorpo` recebeu `distribuicao_matricial: dict | None`. O campo deixa de
ser inerte para elementos funcionais, e e removido de `_campos_inertes` nos
construtores direto e recursivo. A ausencia permanece `None`, sem default
estrutural. O modelo nao executa geometria nem I/O.

Resultado: adequado.

## 14. Modulo geometrico

`tela/distribuicao_matricial.py` concentra o calculo:

```yaml
responsabilidade_unica: sim
io: ausente
dependencia_de_demo: ausente
dependencia_circular: nao_observada
api_publica: calcular_distribuicao, alinhar_na_celula
determinismo: coberto
estado_global: ausente
duplicacao_no_renderer: nao_observada_para_calculo_central
```

## 15. Renderer

O renderer usa `_caixa_de_elemento` como superficie comum para console,
dashboard e lancador quando `distribuicao_matricial` esta presente. A ausencia
preserva os caminhos antigos. O fallback por inviabilidade do motor aciona o
quadro minimo global.

Achado tecnico: a renderizacao do participante corta o texto em
`texto[:cel_w]`, o que introduz truncamento visual no renderer externo.

## 16. Sequencia de calculo

Sequencia material implementada:

1. area util do elemento;
2. participantes imediatos;
3. config ja validada no loader;
4. requisitos minimos por participante;
5. formacoes candidatas;
6. geometria minima;
7. descarte de invalidas;
8. primeiro desempate deterministico;
9. minimos;
10. sobra horizontal;
11. sobra vertical;
12. ordem de expansao;
13. maximos;
14. restos;
15. celulas;
16. alinhamento;
17. renderizacao;
18. fallback.

Restricao violada: na etapa de renderizacao, o renderer externo introduz corte
de conteudo em `minimo_fixo`.

## 17. Formacao

Preferencia por linhas, preferencia por colunas e matriz fixa estao
implementadas e testadas. Matriz fixa nao e reorganizada para caber; se a grade
nao cabe, o motor retorna fallback.

## 18. Ordem

`por_linha` e `por_coluna` preservam a sequencia original dos participantes. Os
testes cobrem ausencia de perda, duplicacao e sobreposicao.

## 19. Dimensionamento

Colunas: `maior_da_coluna`, `uniforme`, `minimo_fixo`.
Linhas: `maior_da_linha`, `uniforme`, `minimo_fixo`.

Os eixos sao independentes no loader e no motor.

## 20. minimo_fixo

Resultado:

```yaml
dimensao_externa_nao_cresce: sim
formacao_nao_invalidada_por_exigencia_interna: sim
participante_recebe_area_calculada: parcialmente
descendentes_nao_reorganizados: sim
truncamento_inventado: sim
quebra_inventada: nao_observada
rolagem_inventada: nao_observada
paginacao_inventada: nao_observada
fallback_interno_propagado: nao_observado
minimos_externos_inviolaveis: sim
```

Defeito: `tela/renderizador.py` corta o texto com `texto[:cel_w]`, e
`tela/teste_renderizador.py` espera esse corte no teste
`test_minimo_fixo_nao_cresce`. Isso viola H-0035 §17 e
`contrato_json_dashboard.md` §9.2.1, que dizem que o renderer externo nao
introduz truncamento, quebra, rolagem ou paginacao como resposta a
`minimo_fixo` excedido.

## 21. Margens e vaos

As quatro margens e os dois vaos sao validados como objetos `{minimo,
maximo?}`; maximo menor que minimo e rejeitado. Horizontal e vertical nao
compartilham politica implicitamente.

## 22. Expansao e restos

`ordem_expansao` e `politica_resto` sao aplicadas por eixo. O teste focal cobre
resto horizontal. Ha cobertura de resto vertical por configuracao e testes do
demo, mas a prova automatizada mais forte esta no motor para o eixo horizontal.

## 23. Alinhamento

Alinhamento horizontal (`inicio`, `centro`, `fim`) e vertical (`topo`,
`centro`, `base`) sao validados e aplicados dentro da celula. Nao substituem a
distribuicao global.

## 24. Dashboard

Participantes imediatos reais: `campos[]` literais do dashboard. Quando o campo
esta presente, `campos[]` e organizado em grade; quando ausente, uma linha por
campo permanece. JSONs produtivos existentes nao foram migrados.

## 25. Console

Quando `distribuicao_matricial` esta presente, o console usa a grade e nao o
placeholder antigo. Quando ausente, preserva `"(console)"`. Politicas
funcionais de navegacao/selecionabilidade nao foram ampliadas neste H-0035.

## 26. Lancador

Quando presente, `distribuicao_matricial` tem precedencia sobre a formacao
historica do lancador. Quando ausente, a politica historica de ADR-0001,
ADR-0002, ADR-0003 e ADR-0023 permanece. H-0034 nao foi corrigido nem declarado
corrigido.

## 27. Fallback

O fallback usa o quadro minimo global por `_quadro_minimo_lancador_ativo`. O
nome e historico, mas comportamento observado atende dashboard, console e
lancador: o teste de dashboard aciona quadro minimo sem contexto de lancador. O
flag e resetado no inicio de `renderizar_tela`, evitando vazamento entre
chamadas.

## 28. Recuperacao

Testes cobrem reducao para quadro minimo e ampliacao com recuperacao, inclusive
pseudo-TTY via `pty.openpty`, `TIOCSWINSZ` e `SIGWINCH`. Validacao humana em TTY
real permanece pendente.

## 29. H-0034

H-0034 nao foi corrigido genericamente, nao foi declarado corrigido, JSON
produtivo principal nao foi migrado e snapshots produtivos nao foram
reescritos. As configuracoes `h0035_lancador_com.json` e
`h0035_lancador_sem.json` sao cenarios proprios de H-0035.

## 30. Configuracoes permanentes

```yaml
configuracoes_esperadas: 26
configuracoes_encontradas: 26
validas: 26
invalidas: []
ausentes: []
adicionais: []
```

Todas as 26 passaram por `python -m json.tool`. O catalogo referencia as 25
telas de conteudo e e separado do demo principal.

## 31. 28 familias

| familia | JSON | teste automatizado | identidade no demo | resultado |
|---|---|---|---|---|
| 1 preferencia_linhas | h0035_pref_linhas | motor/demo/renderer | sim | coberta |
| 2 preferencia_colunas | h0035_pref_colunas | motor/demo | sim | coberta |
| 3 matriz_fixa | h0035_matriz_fixa_cabe | motor/renderer/demo | sim | coberta |
| 4 centralizado_h_colunas | h0035_centralizado_h_colunas | demo | titulo/material | coberta |
| 5 esquerda_margens_min_max | h0035_esquerda_margens_min_max | demo | titulo/material | coberta |
| 6 h_uniforme | h0035_h_uniforme | demo | titulo/material | coberta |
| 7 h_margens_limitadas | h0035_h_margens_limitadas | demo | titulo/material | coberta |
| 8 v_margens_min | h0035_v_margens_min | demo | titulo/material | coberta |
| 9 v_margens_min_max | h0035_v_margens_min_max | demo | titulo/material | coberta |
| 10 v_uniforme | h0035_v_uniforme | demo | titulo/material | coberta |
| 11 um centralizado | h0035_um_centralizado | demo | titulo/material | coberta |
| 12 tres centralizados | h0035_tres_centralizados | demo | titulo/material | coberta |
| 13 quatro centralizados | h0035_quatro_centralizados | demo | titulo/material | coberta |
| 14 matriz fixa cabe | h0035_matriz_fixa_cabe | motor/renderer | sim | coberta |
| 15 matriz fixa quadro minimo | h0035_matriz_fixa_quadro_minimo | demo/pty | sim | coberta |
| 16 recuperacao | h0035_matriz_fixa_quadro_minimo | demo/pty | sim | coberta |
| 17 minimo_fixo excedido | h0035_minimo_fixo_excedido | renderer | sim | coberta com defeito |
| 18 cardinalidade unitaria | h0035_um_centralizado | motor/demo | sim | coberta |
| 19 uma linha | h0035_uma_linha | motor/demo | sim | coberta |
| 20 uma coluna | h0035_uma_coluna | motor/demo | sim | coberta |
| 21 resto horizontal | h0035_resto_horizontal | motor/demo | sim | coberta |
| 22 resto vertical | h0035_resto_vertical | demo | sim | coberta |
| 23 console com campo | h0035_console_com | renderer/demo | sim | coberta |
| 24 console sem campo | h0035_console_sem | renderer/demo | sim | coberta |
| 25 lancador com campo | h0035_lancador_com | renderer/demo | sim | coberta |
| 26 lancador sem campo | h0035_lancador_sem | renderer/demo | sim | coberta |
| 27 dashboard com campo | h0035_dashboard_com | renderer/demo | sim | coberta |
| 28 dashboard sem campo | h0035_dashboard_sem | renderer/demo | sim | coberta |

## 32. Catalogo

`config/telas/demo/h0035_catalogo.json` existe, e um lancador de navegacao, e
referencia todas as 25 telas de conteudo. O teste `demo/teste_demo_distribuicao.py`
confirma catalogo, navegacao e selecao de todas as configuracoes.

## 33. Demo dedicado

`demo/demo_distribuicao.py` e executavel a partir da raiz. Comando smoke
executado:

```text
PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
```

Exit code 0. Saida material exibiu identidade:

```text
identidade: nome=h0035_catalogo familia=(sem distribuicao_matricial) formacao=(n/a) ordem=(n/a) consumidor=lancador estado=normal
```

## 34. Identidade semantica

O demo dedicado calcula identidade por modelo carregado, nao apenas por nome do
arquivo. Testes positivos verificam consumidor dashboard, lancador e console,
formacao, ordem e estado normal/quadro_minimo.

## 35. Testes

Comandos reexecutados:

```yaml
- comando: PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
  exit_code: 0
  verificacoes: 36
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py -q --tb=short
  exit_code: 0
  verificacoes: 287 pytest tests
  falhas: 0
  saida_material: 287 passed, 3 warnings
- comando: PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
  exit_code: 0
  verificacoes: 303
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
  exit_code: 0
  verificacoes: 169
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
  exit_code: 0
  verificacoes: 1184
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py
  exit_code: 0
  verificacoes: 358
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py
  exit_code: 0
  verificacoes: 41
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py
  exit_code: 0
  verificacoes: 22
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py
  exit_code: 0
  verificacoes: 38
  falhas: 0
- comando: PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
  exit_code: 0
  verificacoes: smoke
  falhas: 0
```

## 36. Reconciliacao sete/oito scripts

```yaml
suite_canonica_exigida_pelo_handoff: 8_scripts
scripts_esperados: 8
scripts_realmente_executados: 8
focal_incluido_na_canonica: sim
total_por_script:
  tela/teste_loader.py: 303
  tela/teste_modelo.py: 169
  tela/teste_renderizador.py: 1184
  tela/teste_distribuicao_matricial.py: 36
  demo/teste_demo.py: 358
  demo/teste_diagnostico.py: 41
  demo/teste_demo_distribuicao.py: 22
  demo/teste_explorar_barra_de_menus.py: 38
total_real: 2151
classificacao_da_divergencia: os_oito_scripts_foram_executados;_o_relatorio_separou_o_focal_visualmente
```

## 37. Contagens

O total real por verificacoes impressas pelos scripts e 2151. O comando pytest
focal sobre `tela/teste_renderizador.py` mede testes coletados (287), nao a
metrica interna de verificacoes (1184).

## 38. Independencia dos esperados

O motor usa expectativas manuais e geometrias pequenas fechadas. Porem ha
insuficiencia no teste de `minimo_fixo`: `test_minimo_fixo_nao_cresce` em
`tela/teste_renderizador.py` aceita e confirma o corte visual, quando a norma
exige que o renderer externo nao introduza truncamento.

## 39. Rejeicoes

Loader cobre rejeicoes de classe, mensagem e caminhos materiais. O teste focal
do motor cobre erro de dominio. Nao foi observada renderizacao parcial antes de
erro nas rejeicoes auditadas.

## 40. Pseudo-TTY

`demo/teste_demo_distribuicao.py` usa `pty.openpty`, `fcntl.ioctl` com
`TIOCSWINSZ`, `SIGWINCH`, reducao e ampliacao. Isso e pseudo-TTY real. Nao
substitui a observacao humana em TTY real.

## 41. Regressao

Suites antigas de loader, modelo, renderer, demo, diagnostico e barra de menus
passaram. Ausencia do campo preserva comportamento historico para dashboard,
console e lancador.

## 42. Escopo negativo

Nao observado:

- multinivel;
- heranca;
- cascata;
- migracao automatica;
- reescrita de JSON produtivo;
- correcao de H-0034;
- nova paginacao da capacidade;
- commit.

Violacao observada: truncamento visual inventado pelo renderer externo no
cenario `minimo_fixo`.

## 43. Excecoes

```yaml
excecoes_autorizadas: nenhuma
arquivos_reais_nominalmente_autorizados: sim_para_31_arquivos_da_implementacao
arquivo_fora_da_lista_de_implementacao: nao_confirmado
```

Documentos do ciclo ADR/handoff aparecem no Git, mas sao tratados como
preexistentes ou origem nao confirmada, sem atribuir autoria.

## 44. Validacao manual

```yaml
status: pendente
comando: PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
criterios:
  - abrir catalogo
  - selecionar familias
  - reduzir para quadro minimo
  - ampliar e recuperar
  - observar ordem
  - observar ausencia de perda ou duplicacao
  - comparar politicas
```

O metodo manual e reproduzivel. Como ha achado tecnico, o status final nao pode
ser `I5_MANUAL_VALIDATION_REQUIRED`.

## 45. Estado Git final

Comandos executados apos criar este relatorio:

```text
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff --cached --name-only
git diff --no-index --check /dev/null docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
```

Resultado material da primeira execucao: `git diff --no-index --check` apontou
linha em branco extra no EOF deste relatorio. O arquivo foi corrigido em seguida
sem tocar nos demais artefatos. Estado final esperado apos nova checagem:

```yaml
somente_relatorio_QA_criado_por_esta_etapa: sim
implementacao_inalterada_por_esta_etapa: sim
relatorio_de_implementacao_inalterado_por_esta_etapa: sim
stage: vazio
commit: nao_realizado
git_diff_check: sem_saida_material
git_diff_no_index_check_relatorio: exit_code_1_por_diferenca_contra_dev_null_sem_saida_material
temporarios_novos_no_status: nenhum
```

## 46. Achados

```yaml
achados_bloqueantes: []
achados_altos:
  - id: QA-H0035-IMP-ALTO-001
    severidade: alto
    arquivo: tela/renderizador.py
    secao_ou_simbolo: _linhas_distribuicao_matricial
    evidencia: "linhas 1241-1252 cortam texto do participante com texto[:cel_w]"
    regra_ou_criterio_violado: "H-0035 §17; contrato_json_dashboard.md §9.2.1"
    impacto: "renderer externo introduz truncamento no caso minimo_fixo excedido"
    correcao_necessaria: "remover o truncamento inventado ou delegar o tratamento ao participante/contrato proprio sem violar a distribuicao externa"
    exige_decisao_do_usuario: false
achados_medios:
  - id: QA-H0035-IMP-MEDIO-001
    severidade: medio
    arquivo: tela/teste_renderizador.py
    secao_ou_simbolo: TestDistribuicaoMatricialH0035.test_minimo_fixo_nao_cresce
    evidencia: "linhas 10060-10065 declaram e esperam corte visual em 5 chars"
    regra_ou_criterio_violado: "H-0035 §37.9 e §17"
    impacto: "teste aprova comportamento proibido e nao prova ausencia de truncamento inventado"
    correcao_necessaria: "ajustar expectativa para cobrir o comportamento normativo de minimo_fixo sem truncamento externo"
    exige_decisao_do_usuario: false
achados_baixos:
  - id: QA-H0035-IMP-BAIXO-001
    severidade: baixo
    arquivo: retorno_de_implementacao
    secao_ou_simbolo: contagem_de_arquivos_criados
    evidencia: "retorno declarou 32 criados; Git/lista nominal confirmam 31 criados da implementacao"
    regra_ou_criterio_violado: "fidelidade factual do retorno"
    impacto: "nao ha arquivo extra confirmado; divergencia de resumo"
    correcao_necessaria: "corrigir contagem factual no fechamento da implementacao"
    exige_decisao_do_usuario: false
```

## 47. Observacoes

```yaml
observacoes:
  - id: OBS-QA-H0035-001
    descricao: "O nome _quadro_minimo_lancador_ativo e historico, mas o comportamento observado atende dashboard e lancador; nao e defeito por si so."
  - id: OBS-QA-H0035-002
    descricao: "O pytest focal gerou 287 testes coletados, enquanto o script proprio reporta 1184 verificacoes; sao metricas diferentes."
  - id: OBS-QA-H0035-003
    descricao: ".pytest_cache existe no workspace, mas nao aparece em git status; autoria e criacao nesta etapa nao foram confirmadas."
```

## 48. Conclusao

A implementacao cobre loader, modelo, motor, integracao do renderer, arquivos
autorizados, configuracoes permanentes, demo dedicado, pseudo-TTY e regressao
automatizada. Porem ha defeito tecnico local em `minimo_fixo`: o renderer
externo introduz truncamento visual do participante, e o teste automatizado
aceita esse comportamento. Como a regra e fechada no handoff e nos contratos,
nao ha bloqueio documental; ha necessidade de patch de implementacao.

## 49. Status literal

```text
I2_IMPLEMENTATION_PATCH_REQUIRED
```

## 50. Status normalizado

```text
IMPLEMENTATION_PATCH_REQUIRED
```

## 51. Proxima categoria

```text
PATCH_IMPLEMENTACAO
```
