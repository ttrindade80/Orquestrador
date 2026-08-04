---
name: H-0048-reorganizacao-estrutural-dos-testes-do-renderizador
description: "Handoff 3/3 da ADR-0039 — reorganização estrutural de tela/teste_renderizador.py e dos testes diretamente relacionados, preservando a coleta e a execução legadas"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0048
  data_criacao: 2026-08-03
rastreabilidade:
  contrato_alvo: null
  adr_relacionadas:
    - ADR-0039
  issues_relacionadas:
    - ITEM-0022
  handoffs_anteriores:
    - H-0046
    - H-0047
  sequencia: "3/3"
---

# H-0048 — Reorganizar estruturalmente os testes do renderizador

## 1. Etapa única

Este handoff autoriza exclusivamente:

`IMPLEMENTAR`

Ele não autoriza QA, aprovação, commit ou início do encerramento do
`ITEM-0022`. A criação deste documento é a etapa `CRIAR_HANDOFF`; a próxima
etapa permitida é `QA_HANDOFF`.

## 2. Ordem de autoridade

1. decisão explícita deste pedido;
2. ADR-0039, aceita e aplicada;
3. contratos ativos;
4. H-0046 e H-0047, somente nas fronteiras já fechadas;
5. este handoff.

Qualquer falta, divergência ou decisão nova deve bloquear antes da alteração.
Este documento materializa a atividade como estritamente estrutural:
comportamento, schema, política, interação, API, resultados observáveis,
casos, fixtures, entradas, expectativas e critérios de regressão permanecem
inalterados. Defeitos encontrados durante a implementação devem ser
registrados e deferidos para atividade própria.

## 3. Estado comprovado e estado transportado

```yaml
projeto: Orquestrador
item:
  id: ITEM-0022
  estado: em_andamento

ADR:
  id: ADR-0039
  status: aceita
  aplicacao: ADR_APPLICATION_APPROVED

sequencia:
  passo_1:
    handoff: H-0046
    objeto: modularizacao_estrutural_de_tela_renderizador
    estado: concluido
    commit: 998a133
    suite_completa: 970_passed
  passo_2:
    handoff: H-0047
    objeto: modularizacao_estrutural_de_tela_loader
    estado: concluido
    commit: 5d5d4c7
    testes_focais: 311_passed
    suite_completa: 970_passed
    demonstracao: 7_de_7
  passo_3:
    handoff: H-0048
    objeto: reorganizacao_estrutural_dos_testes_do_renderizador
    estado: atual

baseline:
  branch: master
  HEAD: 5d5d4c794508b1981f5fa65be079b8db748c6064
  stage: vazio
  alteracoes_rastreadas: nenhuma
  nao_rastreados_preexistentes_preservados:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_BACKLOG_ITENS_POSSIVELMENTE_JA_REALIZADOS_2026-08-03.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/distribuicao_matricial.cpython-314.pyc
    - tela/__pycache__/loader.cpython-314.pyc
    - tela/__pycache__/modelo.cpython-314.pyc
    - tela/__pycache__/renderizador.cpython-314.pyc

proxima_etapa_permitida_apos_esta_execucao: QA_HANDOFF
```

O relatório auxiliar de backlog e os cinco `.pyc` não fazem parte do objeto
do handoff e não podem ser lidos, alterados, removidos ou incluídos no scope.
Os passos 1 e 2 estão fechados e não devem ser reabertos. A implementação não
é autorizada a alterar a produção modularizada pelos passos anteriores.

## 4. Capacidade coesa

Reorganizar estruturalmente as 13.960 linhas de
`tela/teste_renderizador.py` em módulos de teste agrupados por
responsabilidades reais já materializadas em `tela/renderizacao/`, mantendo
`tela/teste_renderizador.py` como fachada de coleta, execução direta e
agregação compatível. A operação deve preservar integralmente a suíte, os
modos de execução, a identidade nominal dos casos, fixtures, entradas,
expectativas, mensagens, snapshots/quadros literais, parametrizações
existentes e critérios de regressão.

O tamanho atual é diagnóstico, não critério de divisão. Nenhum módulo pode
ser definido por faixa de linhas, ordem histórica, quantidade semelhante de
linhas ou pelo simples fato de consumir `renderizar_tela`.

## 5. Manifesto fechado de leitura

### 5.1 Leitura integral obrigatória

Foram lidos integralmente para esta autoria:

```yaml
leitura_integral:
  - docs/adr/ADR-0039-modularizacao-estrutural-do-runtime-de-telas.md
  - docs/backlog.md [somente o bloco integral do ITEM-0022]
  - docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md
  - docs/handoff/H-0047-modularizacao-estrutural-do-loader.md
  - tela/teste_renderizador.py
```

O implementador pode reler somente esses arquivos e os focos abaixo para
executar a autorização. O relatório acumulado de backlog continua fora da
leitura.

### 5.2 Template canônico

O índice vigente `docs/templates/00_INDICE_TEMPLATES_DOCUMENTAIS_E_RELATORIOS.md`
identifica `docs/templates/TEMPLATE_HANDOFF_IMPLEMENTACAO.md` como o template
canônico de autorização de implementação. O frontmatter e as seções deste
handoff seguem esse template; os detalhes específicos abaixo fecham o
diagnóstico do H-0048.

### 5.3 Leitura focal autorizada

```yaml
leitura_focal:
  - arquivo: tela/renderizacao/*.py
    comando_busca: printf '%s\n' tela/renderizacao/*.py
    objetivo: confirmar nomes reais, proprietários, relações e pontos whitebox já materializados pelo H-0046
  - arquivo: pyproject.toml|pytest.ini|setup.cfg|tox.ini
    comando_busca: verificar focalmente nessa ordem quais existem e ler somente descoberta, testpaths, addopts, markers e importação
    objetivo: compatibilizar a organização com a coleta real
  - arquivo: tela/teste_*.py e demo/teste_*.py
    comando_busca: rg -n 'tela\.teste_renderizador|from tela import teste_renderizador|import tela\.teste_renderizador|teste_renderizador\.py' tela/teste_*.py demo/teste_*.py
    objetivo: localizar consumidores nominais do caminho legado
  - arquivo: tela/teste_*.py e demo/teste_*.py
    comando_busca: rg -n 'from tela\.renderizador import|import tela\.renderizador|tela\.renderizador\.' tela/teste_*.py demo/teste_*.py
    objetivo: classificar consumidores da fachada pública
  - arquivo: tela/teste_*.py e demo/teste_*.py
    comando_busca: rg -n 'from tela\.renderizacao|import tela\.renderizacao|tela\.renderizacao\.' tela/teste_*.py demo/teste_*.py
    objetivo: classificar inspeções diretas do subpacote já modularizado
```

Não ler `docs/relatorios/RELATORIO_LEVANTAMENTO_BACKLOG_ITENS_POSSIVELMENTE_JA_REALIZADOS_2026-08-03.md`, relatórios de implementação ou QA, módulos de nomenclatura não autorizados, contratos não necessários para esta classificação, nem produção fora dos focos acima.

## 6. Diagnóstico factual do monólito

### 6.1 Inventário AST

O inventário AST do arquivo atual registrou:

| Item | Quantidade | Observação |
|---|---:|---|
| linhas físicas | 13.960 | indicador de concentração, não arquitetura |
| imports de nível superior | 17 | stdlib, `tela.loader`, `tela.modelo`, fachada `tela.renderizador`, pytest/imports tardios nominais |
| atribuições/estruturas de módulo | 24 | estados, estilos, expected outputs, catálogos e parâmetros |
| funções de nível superior | 120 | 72 coletáveis, 47 helpers e `main` |
| classes de teste | 21 | todas iniciam com `Test` |
| métodos de teste | 299 | nomes iniciados por `test` |
| testes coletáveis no monólito | 371 | 72 funções + 299 métodos |
| fixtures pytest | 1 | `_fixture_h0041_qa002`, nome público `fixture_h0041_qa002` |
| parametrizações | 0 | nenhum decorator `pytest.mark.parametrize` encontrado |
| entry points | 1 | `main()` do runner direto |
| guards de execução | 1 | `if __name__ == "__main__": sys.exit(main())` |
| monkeypatch/mock/patch | 0 | nenhum uso foi encontrado |
| leituras `read_text` | 10 | inspeções whitebox de produção e renderização modularizada |
| leituras `open` | 1 | fixture/JSON focal |
| `inspect.getsource` | 1 | inspeção de `tela.renderizacao.matriz_participantes` |
| `importlib.import_module` | 2 | inspeções diretas de `tela.renderizacao.matriz_participantes` |

As 21 classes e sua transferência integral são:

| Classe | Faixa factual atual | métodos totais / métodos `test_*` | proprietário futuro |
|---|---:|---:|---|
| `TestLinhasBarra` | 1382–1829 | 30 / 27 | `barra_menus.py` |
| `TestDistribuicaoH0018` | 1832–2448 | 38 / 35 | `barra_menus.py` |
| `TestArranjoH0019` | 2476–2816 | 16 / 13 | `composicao_corpo.py` |
| `TestPreenchimentoVerticalH0020` | 2819–3160 | 17 / 12 | `composicao_corpo.py` |
| `TestPreenchimentoBordeadoH0021` | 3163–3567 | 18 / 14 | `composicao_corpo.py` |
| `TestDistribuicaoVerticalH0025` | 3602–4080 | 27 / 22 | `composicao_corpo.py` |
| `TestDistribuicaoHorizontalH0026` | 4083–4525 | 20 / 16 | `composicao_corpo.py` |
| `TestHierarquiaGruposH0027` | 4629–5213 | 21 / 19 | `composicao_corpo.py` |
| `TestRenderizadorMatrizH0028` | 5216–5407 | 11 / 8 | `matriz_participantes.py` |
| `TestCardinalidadeUnitariaH0029` | 5442–6002 | 24 / 20 | `matriz_participantes.py` |
| `TestTelasPermanentesH0029` | 6089–6568 | 14 / 12 | `matriz_participantes.py` |
| `TestCatalogoH0030` | 6596–7450 | 11 / 8 | `matriz_participantes.py` |
| `TestDistribuicaoResponsivaH0034` | 7619–8630 | 17 / 14 | `lancador.py` |
| `TestOcupacaoIntegralCorpoH0033` | 8665–9147 | 27 / 22 | `composicao_corpo.py` |
| `TestHelperHorizontalH0033Patch2` | 9150–9395 | 16 / 10 | `composicao_corpo.py` |
| `TestCardinalidadeHorizontalH0033Patch3` | 9398–9616 | 11 / 6 | `composicao_corpo.py` |
| `TestCardinalidadeHorizontalH0033Patch4` | 9619–10015 | 12 / 7 | `composicao_corpo.py` |
| `TestDistribuicaoMatricialH0035` | 10018–10427 | 16 / 12 | `matriz_participantes.py` |
| `TestRotuloDinamicoEscP21` | 13565–13807 | 11 / 11 | `selecao.py` |
| `TestH0045P23BarraCincoLinhas` | 13851–13944 | 10 / 10 | `barra_menus.py` |
| `TestH0045P23RegressaoDuasLinhas` | 13947–13960 | 1 / 1 | `barra_menus.py` |

Os números fecham 299 métodos de teste e 21 classes; nenhuma classe pode ser
dividida, renomeada ou parcialmente copiada. Métodos auxiliares não
coletáveis pertencentes às classes permanecem com sua classe proprietária.

### 6.2 Estados, constantes e estruturas

A propriedade única das atribuições atuais será preservada assim:

```yaml
fachada:
  - sys.dont_write_bytecode [mecanismo preexistente de execução direta]
comum:
  - _BASE_PADRAO
  - _RESULTADOS
  - _RAIZ_TELAS_DEMO
  - _ESTILO_CURVA
  - _ESTILO_RETA
  - _ESTILO_CAIXA_ALTA
  - _ESTILO_H0044
  - _EXPECTED_ORQUESTRADOR
  - _EXPECTED_ORQUESTRADOR_RETA
  - _PARAMS_LANCADOR_DEMO [compartilhada entre fundamentos e lançador]
composicao_corpo:
  - _H0033_TELAS_TODAS
  - _H0033_TELAS_MATRIZ
  - _H0033_TELAS_ALTURA_NATURAL
  - _H0033_TELAS_ALTURA_20
matriz_participantes:
  - _H0029_TELAS_DASHBOARD
  - _H0029_TELAS_GRUPO_DISTRIBUIDO
  - _H0029_TELAS_GRUPO_SEM_DIST
  - _H0029_TELAS_TODAS
  - _TELAS_H0030
  - _GEO_H0030
  - _ALTURA_MATRIZ_H0030
lancador:
  - _H0034_ITENS_DEMO
integracao:
  - _DM_H0045_P07
```

`_RESULTADOS` continua sendo uma única lista compartilhada por todos os
testes manuais do runner. `_registrar` e `_espera_excecao` são proprietários
de `comum.py`; não podem ser duplicados. Fábricas ou helpers consumidos por
mais de um grupo têm um único proprietário em `comum.py`:

```text
_modelo_orquestrador_sem_distribuicao
_funcional
_grupo
_grupo_matriz_render_h0028
_modelo_h0029
_h0029_linhas_totais
_alturas_caixas
_corpo_alturas
```

Os helpers de um único domínio permanecem no módulo desse domínio. Entre
eles estão `_dist_canonica` e `_chip` (barra), `_modelo_horizontal`
(composição), os helpers `_h0029_*` de
catálogo não compartilhados (matriz), os `_h0034_*` (lançador), os helpers
`_modelo_com_conteudo`, `_linhas_caixa_console` e `_texto_caixa_console`
(conteúdo), os helpers `_carregar_fixture_h0041_*`, `_chip_enter_fixture`,
`_renderizar_h0041_p03`, `_barra_chip`, `_carregar_fixture_p21` e
`_barra_esc_p21` (seleção), e os helpers `_console_paginado_h0045p07`,
`_grupo_h0045p07`, `_p12_montar_caso_render`, `_caixa_console_paginado_ph07`
e `_margens_estruturais_ph07` (integração). Não duplicar nenhum deles.

```yaml
cadeia_de_alturas:
  _alturas_caixas:
    consumidor_direto_unico: _corpo_alturas
  _corpo_alturas:
    consumidores:
      - composicao_corpo.py
      - matriz_participantes.py
  consumidor_em_lancador.py: false
```

### 6.3 Modos de execução vigentes

Foram confirmados factual e nominalmente estes modos:

```text
python tela/teste_renderizador.py
python -m pytest tela/teste_renderizador.py
python -m pytest
```

O primeiro é um runner próprio: imprime cabeçalho, executa a sequência
explícita de verificações até H-0041, imprime total/passaram/falharam e
retorna `0` quando não há falhas e `1` caso contrário. Ele não executa os
casos H-0044/H-0045 que aparecem depois da definição histórica de `main()`;
essa diferença é parte do comportamento vigente e deve permanecer.

O segundo modo coleta os 371 casos do monólito. O terceiro coleta a suíte
canônica completa, cujo baseline transportado é 970 testes aprovados.

### 6.4 Whitebox e relações entre helpers

Não foram encontrados monkeypatches, `unittest.mock`, `patch` ou alteração
de `sys.modules`. Foram encontrados:

```yaml
leituras_de_producao:
  - tela/renderizador.py [proibições de leitura/importação, fonte hardcoded, inércia e regressões H-0045]
  - tela/renderizacao/contexto_execucao.py [presença de acesso declarativo]
  - tela/renderizacao/matriz_participantes.py [acesso declarativo e getsource/importação]
  - tela/renderizacao/barra_menus.py [acesso declarativo e estilo ANSI]
leituras_de_entrada:
  - JSON/configuração nominal de H-0029 via Path.open
inspeções_de_importação:
  - importlib.import_module("tela.renderizacao.matriz_participantes") em dois casos
```

Essas inspeções pertencem aos casos que as executam e devem ser transferidas
com seus corpos e strings intactos. Os caminhos de produção continuam sendo
os caminhos já fechados por H-0046; o caminho do monólito de testes não é
inspecionado por nenhum consumidor externo material.

A fixture `_fixture_h0041_qa002`, definida uma única vez em `selecao.py`,
é registrada também no namespace da fachada por meio de importação nominal
(`from tela.testes_renderizador.selecao import _fixture_h0041_qa002 as
_fixture_h0041_qa002`), sem segunda definição, wrapper ou duplicação. Ver
8.2 e 8.3.

### 6.5 Responsabilidades reais

| Responsabilidade | Evidência atual | Módulo de teste proprietário |
|---|---|---|
| primitivas de texto, ANSI, largura e alinhamento | top-level inicial, `TestLinhasBarra`, H-0044 e inspeções de ANSI | `fundamentos.py` e `barra_menus.py` |
| caixas, geometria e distribuição de área | H-0019, H-0020, H-0021, H-0025 e H-0026 | `composicao_corpo.py` |
| renderização e estado visual de barra de menus | H-0016/H-0018, H-0044 chips, H-0045 P01/P02 e P23 | `barra_menus.py` |
| contexto, seleção e indicadores de console | H-0041 e H-0045 P21 | `selecao.py` |
| console, fragmentos e integração de página | H-0045 P04/P06/P07/P10/P11/P12/PH07 | `integracao.py` |
| conteúdo externo, designadores e truncamento | H-0036, H-0037 e H-0044 P01 | `conteudo_externo.py` |
| lançador, fila, matriz responsiva e parâmetros de texto | H-0034 | `lancador.py` |
| distribuição matricial e catálogos de telas | H-0028, H-0029, H-0030 e H-0035 | `matriz_participantes.py` |
| composição transversal, grupos, ocupação e cardinalidade | H-0027 e H-0033 | `composicao_corpo.py` |
| smoke inicial, fachada e resultados observáveis básicos | H-0006/H-0007/H-0009/H-0010A/H-0015 | `fundamentos.py` |

Casos de integração continuam nos proprietários acima quando atravessam
mais de um módulo de produção; não são forçados para um módulo de tamanho
parecido. O módulo `integracao.py` existe porque H-0045 cruza console,
geometria, paginação interna, barra e seleção.

## 7. Classificação de testes diretamente relacionados

### 7.1 Arquivos localizados

As buscas fechadas localizaram estes arquivos:

```yaml
arquivos:
  - tela/teste_navegacao.py
  - tela/teste_paginacao.py
  - tela/teste_renderizador.py
  - tela/teste_resultado_execucao.py
  - demo/teste_demo.py
  - demo/teste_demo_console.py
  - demo/teste_demo_console_modos.py
  - demo/teste_demo_navegacao.py
  - demo/teste_demo_paginacao.py
  - demo/teste_demo_selecao.py
  - demo/teste_diagnostico.py
  - demo/teste_explorar_barra_de_menus.py
```

### 7.2 Classificação nominal

```yaml
classificacao:
  migrados_do_monolito:
    - tela/teste_renderizador.py [somente definições transferidas; o caminho permanece como fachada]
  relacionados_preservados_sem_alteracao:
    - tela/teste_navegacao.py
    - tela/teste_paginacao.py
    - tela/teste_resultado_execucao.py
    - demo/teste_demo.py
    - demo/teste_demo_console.py
    - demo/teste_demo_console_modos.py
    - demo/teste_demo_navegacao.py
    - demo/teste_demo_paginacao.py
    - demo/teste_demo_selecao.py
    - demo/teste_diagnostico.py
    - demo/teste_explorar_barra_de_menus.py
  relacionados_com_ajuste_focal_autorizado: []
```

Os arquivos externos importam símbolos da fachada pública `tela.renderizador`
ou mencionam nominalmente o caminho legado em texto diagnóstico. Nenhum
importa helper definido em `tela/teste_renderizador.py`, inspeciona
nominalmente o caminho do monólito de testes em execução, depende da
coabitação física de um chamador e chamado dentro desse arquivo ou exige
atualização mecânica para preservar seu caso. A fachada pública de produção
continua inalterada. Portanto, nenhum teste externo recebe ajuste focal.
Um arquivo que apenas consome `renderizar_tela` permanece preservado.

## 8. Arquitetura-alvo nominal

### 8.1 Subpacote e arquivos

O novo subpacote é necessário porque os módulos precisam compartilhar
fixtures/helpers internos sem exportá-los como módulos de produção. Os nomes
não começam por `teste_` deliberadamente: `pytest.ini` só descobre
`teste_*.py`; a fachada legada fará a agregação única no modo canônico,
preservando a coleta por `tela/teste_renderizador.py` e evitando coleta dupla.
Os módulos continuam executáveis como caminhos explícitos do pytest.

```text
tela/testes_renderizador/__init__.py
tela/testes_renderizador/comum.py
tela/testes_renderizador/fundamentos.py
tela/testes_renderizador/barra_menus.py
tela/testes_renderizador/composicao_corpo.py
tela/testes_renderizador/matriz_participantes.py
tela/testes_renderizador/lancador.py
tela/testes_renderizador/conteudo_externo.py
tela/testes_renderizador/selecao.py
tela/testes_renderizador/integracao.py
tela/testes_renderizador/runner.py
```

`__init__.py` fica sem lógica e sem reexportação de testes. `comum.py` não
contém testes coletáveis; contém apenas o estado, estilos, expected outputs,
fábricas e helpers compartilhados nominalmente fechados. `runner.py` não
contém testes coletáveis; contém a função `main` e a ordem de execução direta.

### 8.2 Conteúdo transferido por módulo

#### `comum.py`

Proprietário único de `_BASE_PADRAO`, `_RESULTADOS`, `_RAIZ_TELAS_DEMO`,
`_ESTILO_CURVA`, `_ESTILO_RETA`, `_ESTILO_CAIXA_ALTA`, `_ESTILO_H0044`,
`_EXPECTED_ORQUESTRADOR`, `_EXPECTED_ORQUESTRADOR_RETA`,
`_PARAMS_LANCADOR_DEMO`, `_registrar`, `_espera_excecao`,
`_modelo_orquestrador_sem_distribuicao`, `_funcional`, `_grupo`,
`_grupo_matriz_render_h0028`, `_modelo_h0029`, `_h0029_linhas_totais`,
`_alturas_caixas` e `_corpo_alturas`. Os consumidores importam esses nomes de
`comum.py`; não há cópia local. `_alturas_caixas` e `_corpo_alturas` formam
uma cadeia coesa compartilhada entre composição e matriz. Seus imports de
produção ficam restritos a `tela.loader` e `tela.modelo`, além da stdlib; não
há importação de fachada, runner, módulo proprietário ou qualquer outro
módulo de produção.

#### `fundamentos.py`

Transfere integralmente estas 11 funções coletáveis:

```text
teste_renderizador_orquestrador
teste_renderizador_destino_minimo
teste_renderizador_grupo_minimo
teste_modelo_fabricado
teste_erros_renderizador
teste_proibicoes_importacao
teste_inspecao_fonte_hardcoded
teste_inercia
teste_alternancia_borda
teste_largura_explicita
teste_altura_explicita
```

Conserva os casos de smoke do modelo, saída literal, borda, largura/altura,
proibições de importação/leitura, inércia e o consumo declarativo de
`EstiloResolvido`. Usa os símbolos de renderização pela fachada pública;
inspeções já autorizadas de produção mantêm os caminhos materializados por
H-0046.

#### `barra_menus.py`

Transfere integralmente `TestLinhasBarra` (27 testes),
`TestDistribuicaoH0018` (35 testes), `TestH0045P23BarraCincoLinhas` (10
testes) e `TestH0045P23RegressaoDuasLinhas` (1 teste). Transfere também os 8
testes top-level H-0044 de chips destacados/ativos/inativos e os 3 testes
top-level H-0045 de fragmentos/chips/barra alinhada:

```text
test_h0044_chip_destacado_usa_cor_alerta
test_h0044_chip_ativo_normal_sem_destaque
test_h0044_chip_inativo_cinza_nao_amarelo
test_h0044_destaque_nao_inativa
test_h0044_largura_sem_ansi_destaque
test_h0044_cor_nao_vaza_entre_chips
test_h0044_executar_disponivel_ativa_selecao_nao_vazia
test_h0044_regressao_sem_destaque_identica
test_h0045_renderiza_apenas_fragmentos_da_pagina_atual_com_indicador
test_h0045_p01_chips_pagina_visiveis_na_pagina_1_com_anterior_inativo
test_h0045_p02_barra_alinhada_na_sequencia_de_larguras
```

Seus helpers exclusivos são `_dist_canonica`, `_chip`,
`_h0045_linha_barra_menus`, `_modelo_fluxo_paginado_p23` e
`_preparar_ctx_p23`. Total proprietário: 84 casos coletáveis.

#### `composicao_corpo.py`

Transfere integralmente `TestArranjoH0019` (13),
`TestPreenchimentoVerticalH0020` (12), `TestPreenchimentoBordeadoH0021`
(14), `TestDistribuicaoVerticalH0025` (22),
`TestDistribuicaoHorizontalH0026` (16), `TestHierarquiaGruposH0027` (19),
`TestOcupacaoIntegralCorpoH0033` (22), `TestHelperHorizontalH0033Patch2`
(10), `TestCardinalidadeHorizontalH0033Patch3` (6) e
`TestCardinalidadeHorizontalH0033Patch4` (7). Total proprietário: 141
casos coletáveis.

O helper local `_modelo_horizontal` e as constantes `_H0033_*` permanecem
aqui. `_alturas_caixas` e `_corpo_alturas` são importados de `comum.py`; não
é criada nenhuma dependência de `matriz_participantes.py`, nem duplicação,
wrapper ou importação entre composição e matriz para obter esses helpers. As fábricas
compartilhadas listadas em `comum.py` são importadas, nunca duplicadas.
#### `matriz_participantes.py`

Transfere integralmente `TestRenderizadorMatrizH0028` (8),
`TestCardinalidadeUnitariaH0029` (20), `TestTelasPermanentesH0029` (12),
`TestCatalogoH0030` (8) e `TestDistribuicaoMatricialH0035` (12). Total
proprietário: 60 casos coletáveis.

Os catálogos `_H0029_*`, `_TELAS_H0030`, `_GEO_H0030` e
`_ALTURA_MATRIZ_H0030` permanecem neste arquivo. Seus helpers de JSON e
geometria são transferidos integralmente, com proprietário único:
`_h0029_caminho_json`, `_h0029_dashboard_topo`, `_h0029_dashboard_base`,
`_h0029_barra_topo` e `_h0029_bordas_laterais_continuas`. Os casos que
consomem `_corpo_alturas` importam esse helper de `comum.py`; este módulo não
consome `_alturas_caixas`.

#### `lancador.py`

Transfere integralmente `TestDistribuicaoResponsivaH0034` (14 testes),
incluindo todos os testes de fila, matriz responsiva, quadro mínimo,
alinhamento, parâmetros, caminho legado e proibições de importação. Os
helpers `_h0034_modelo_lancador`, `_h0034_modelo_isolado`,
`_h0034_row_of` e `_h0034_modelo_alinhamento`, além de
`_H0034_ITENS_DEMO`, têm este proprietário. `_PARAMS_LANCADOR_DEMO` é
importado de `comum.py` por também ser usado pelos fundamentos.

`lancador.py` não consome `_alturas_caixas` nem `_corpo_alturas`. Seus 14
testes e helpers próprios permanecem inalterados.

#### `conteudo_externo.py`

Transfere as 4 funções coletáveis H-0036/H-0037:

```text
teste_conteudo_externo_h0036_render
teste_h0037_manual_001_marcador_truncamento
teste_h0037_manual_002_esc_primeiro
teste_h0037_qapp7_verb_sem_corte_silencioso
```

Transfere os 8 testes top-level `test_h0044_p01_*` sobre valor de campo,
envelope e redimensionamento. `_modelo_com_conteudo`,
`_linhas_caixa_console` e `_texto_caixa_console` são locais. Total
proprietário: 12 casos coletáveis.

`teste_h0037_qapp7_verb_sem_corte_silencioso` continua definido uma única
vez neste módulo, integra seu `__all__` normal como teste proprietário e pode
ser importado por alias privado exclusivamente por `integracao.py`; essa
importação não altera a propriedade do teste.

#### `selecao.py`

Transfere `teste_selecao_multipla_h0041`, os 7 testes
`test_qah0041_002_*`, os 11 testes H-0041 manual/P04 e
`TestRotuloDinamicoEscP21` (11 testes). Total proprietário: 30 casos
coletáveis. O fixture `_fixture_h0041_qa002` permanece definido uma única
vez com o nome pytest `fixture_h0041_qa002`; seus consumidores continuam
resolvendo pelo mesmo nome. Proprietário único: `selecao.py`; duplicação,
renomeação ou wrapper são proibidos. `_fixture_h0041_qa002` não integra o
`__all__` de `selecao.py`; a fachada a importa nominalmente, fora da
agregação por `__all__` (ver 8.2, fachada).

#### `integracao.py`

Transfere os 19 testes H-0045 que não são de barra: P04, P06, P07, P10,
P11, P12 e PH07, nominalmente:

```text
test_h0045_p04_dois_consoles_ids_unicos_foco_cursor_e_paginas_independentes
test_h0045_p06_distribuicao_vertical_geometria_por_console_e_renderer_concordam
test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao
test_h0045_p07_console_direto_preservado_regressao
test_h0045_p07_console_dentro_de_grupo_geometria_real
test_h0045_p07_dois_consoles_mesmo_grupo_geometrias_independentes
test_h0045_p07_grupo_aninhado_geometria_considera_ancestrais
test_h0045_p07_console_ausente_retorna_none_sem_fallback
test_h0045_p07_estrutura_matriz_geometria_por_celula
test_h0045_p10_mapa_fisico_usa_largura_da_celula_e_preserva_fragmentos
test_h0045_p11_conjunto_vazio_chips_pagina_visiveis_e_inativos
test_h0045_p12_quebra_textual_por_largura_marcadores_unicos
test_h0045_p12_continuacao_sem_cursor_regular_e_alta
test_h0045_p12_vazio_chips_visiveis_inativos_e_autoridade_geometrica
test_h0045_ph07_largura_horizontal_celula_unica_quatro_larguras
test_h0045_ph07_coerencia_renderer_mapa_fisico
test_h0045_ph07_distribuicao_matricial_multiplas_celulas_preservada
test_h0045_ph07_regressao_h0037_console_externo
test_h0045_ph07_cinco_telas_validacao
```

Os helpers `_console_paginado_h0045p07`, `_grupo_h0045p07`,
`_p12_montar_caso_render`, `_caixa_console_paginado_ph07` e
`_margens_estruturais_ph07`, e `_DM_H0045_P07`, permanecem aqui. Total
proprietário: 19 casos coletáveis.

```yaml
importacao_de_proprietario_autorizada:
  modulo: conteudo_externo.py
  simbolo: teste_h0037_qapp7_verb_sem_corte_silencioso
  alias: _teste_h0037_qapp7_verb_sem_corte_silencioso
  consumidor: test_h0045_ph07_regressao_h0037_console_externo
```

O alias não integra `__all__`, não é coletável, não é definição e não pode
ser usado por outro caso. Ele não autoriza outras dependências entre
proprietários.

Forma nominal autorizada:

```python
from tela.testes_renderizador.conteudo_externo import (
    teste_h0037_qapp7_verb_sem_corte_silencioso
    as _teste_h0037_qapp7_verb_sem_corte_silencioso,
)
```

No caso consumidor, a chamada autorizada é
`_teste_h0037_qapp7_verb_sem_corte_silencioso()`; argumentos, ordem, controle
de fluxo e demais instruções permanecem idênticos.

#### `runner.py`

Transfere somente `main()` e sua composição de execução direta. O corpo deve
preservar a ordem nominal atual:

```text
teste_renderizador_orquestrador
teste_renderizador_destino_minimo
teste_renderizador_grupo_minimo
teste_modelo_fabricado
teste_erros_renderizador
teste_proibicoes_importacao
teste_inspecao_fonte_hardcoded
teste_inercia
teste_alternancia_borda
teste_largura_explicita
teste_altura_explicita
TestLinhasBarra, TestDistribuicaoH0018, TestArranjoH0019,
TestPreenchimentoVerticalH0020, TestPreenchimentoBordeadoH0021,
TestDistribuicaoVerticalH0025, TestDistribuicaoHorizontalH0026,
TestHierarquiaGruposH0027, TestRenderizadorMatrizH0028,
TestCardinalidadeUnitariaH0029, TestTelasPermanentesH0029,
TestCatalogoH0030, TestDistribuicaoResponsivaH0034,
TestOcupacaoIntegralCorpoH0033, TestHelperHorizontalH0033Patch2,
TestCardinalidadeHorizontalH0033Patch3,
TestCardinalidadeHorizontalH0033Patch4, TestDistribuicaoMatricialH0035
teste_conteudo_externo_h0036_render
teste_h0037_manual_001_marcador_truncamento
teste_h0037_manual_002_esc_primeiro
teste_h0037_qapp7_verb_sem_corte_silencioso
teste_selecao_multipla_h0041
```

O resumo usa `_RESULTADOS` de `comum.py` e conserva os textos, códigos de
saída e comportamento de falha atuais. `runner.py` não importa a fachada de
teste; seus imports apontam para os proprietários.

#### `tela/teste_renderizador.py`

Permanece como fachada compatível de execução e agregação, contendo somente:

1. docstring e o mecanismo preexistente `sys.dont_write_bytecode = True`;
2. a preparação preexistente da raiz para `python tela/teste_renderizador.py`;
3. importações explícitas dos símbolos `__all__` dos oito módulos
   proprietários, para que o caminho legado continue sendo o proprietário de
   coleta no `pytest.ini` atual;
4. importação nominal de
   `from tela.testes_renderizador.selecao import _fixture_h0041_qa002 as
   _fixture_h0041_qa002`, exclusivamente para que o pytest encontre e
   registre a fixture no namespace da fachada;
5. importação de `main` de `runner.py`;
6. o guard `if __name__ == "__main__": sys.exit(main())`.

Não definir funções, classes, fixtures ou helpers no arquivo. A importação
nominal do item 4 é uma referência ao objeto definido em `selecao.py`, não
uma redefinição; `_fixture_h0041_qa002` continua tendo proprietário único.
O agregador não usa importação genérica que exponha produção ou helpers
acidentalmente: cada módulo proprietário declara `__all__` apenas com seus
testes/classes, e a fixture é importada fora dessa agregação. Nenhum outro
helper privado é importado pela fachada. Os módulos do subpacote não iniciam
por `teste_`, portanto não são descobertos independentemente pelo padrão
`python_files = teste_*.py`; quando um deles é passado explicitamente ao
pytest, seus testes são executáveis. Isso preserva simultaneamente o caminho
legado, o conjunto completo e a propriedade única.

### 8.3 Direção de imports

```text
tela/teste_renderizador.py
    ├── oito módulos proprietários
    ├── fixture nominal de selecao.py
    └── main de runner.py

runner.py
    ├── comum.py
    └── módulos proprietários necessários à sequência histórica

composicao_corpo.py
    └── comum.py e produção pública vigente

matriz_participantes.py
    └── comum.py e produção pública vigente

integracao.py
    ├── comum.py e produção pública vigente
    └── conteudo_externo.py
        [somente alias privado do teste H-0037 autorizado]

demais módulos proprietários
    └── comum.py e produção pública vigente

comum.py
    └── stdlib, tela.loader e tela.modelo
```

A importação nominal de `_fixture_h0041_qa002` continua sendo uma referência
ao objeto definido em `selecao.py`, não uma importação de helper para uso
funcional pela fachada. A única dependência proprietário → proprietário é
`integracao.py → conteudo_externo.py`; ela preserva uma chamada direta
existente no monólito. Nenhum proprietário pode importar outro para obter
helper e nenhuma outra exceção é implícita. Não criar ciclo, `sys.path` novo,
import absoluto dependente do ambiente, caminho `/home/...`, nem importação
da fachada ou do runner por proprietários. As duas inspeções whitebox diretas
de `tela.renderizacao.matriz_participantes` permanecem porque já são casos
estruturais explícitos; elas não migram consumidores de produção.
## 9. Escopo nominal da futura implementação

### 9.1 Arquivos alterados

Autorize nominalmente:

```text
tela/teste_renderizador.py
```

### 9.2 Diretório e arquivos criados

Autorize nominalmente:

```text
tela/testes_renderizador/
tela/testes_renderizador/__init__.py
tela/testes_renderizador/comum.py
tela/testes_renderizador/fundamentos.py
tela/testes_renderizador/barra_menus.py
tela/testes_renderizador/composicao_corpo.py
tela/testes_renderizador/matriz_participantes.py
tela/testes_renderizador/lancador.py
tela/testes_renderizador/conteudo_externo.py
tela/testes_renderizador/selecao.py
tela/testes_renderizador/integracao.py
tela/testes_renderizador/runner.py
```

### 9.3 Relatório da implementação

Autorize:

```text
docs/relatorios/IMP-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
```

### 9.4 Arquivos relacionados preservados

Registre nominalmente, sem alteração:

```text
tela/teste_navegacao.py
tela/teste_paginacao.py
tela/teste_resultado_execucao.py
demo/teste_demo.py
demo/teste_demo_console.py
demo/teste_demo_console_modos.py
demo/teste_demo_navegacao.py
demo/teste_demo_paginacao.py
demo/teste_demo_selecao.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
```

### 9.5 Produção preservada

Proíba alterações em:

```text
tela/renderizador.py
tela/renderizacao/**
tela/loader.py
tela/carregamento/**
tela/modelo.py
tela/paginacao.py
tela/navegacao.py
tela/selecao.py
config/**
docs/adr/**
docs/contratos/**
docs/nomenclatura/**
docs/backlog.md
docs/HISTORICO.md
```

Preserve sem leitura ou alteração:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_BACKLOG_ITENS_POSSIVELMENTE_JA_REALIZADOS_2026-08-03.md
tela/__pycache__/*.pyc
```

Nenhum arquivo externo recebe ajuste focal.

## 10. Entradas, fixtures, temporários e saídas

Registre:

```yaml
entradas_reais:
  - tela/teste_renderizador.py
  - configuração e fixtures já consumidas pelos testes existentes

fixtures:
  politica: preservar caminhos, conteúdo, identidade e consumidores
  criacao_de_novas_fixtures: proibida
  remocao_ou_substituicao: proibida

temporarios:
  pytest: somente saída transitória não persistente
  compilacao: totalmente em memória
  importacao: sem gravação de bytecode
  pyc_novos: proibidos
  novos___pycache__: proibidos
  persistencia: proibida
  limpeza: não remover resíduos preexistentes fora do escopo

saidas_persistentes:
  - módulos reorganizados
  - fachada compatível
  - relatório de implementação

saidas_de_teste:
  politica: não preservar dumps, caches ou snapshots novos
```

## 11. Mapa obrigatório de transferência

Exija da implementação um mapa completo e verificável contendo, para cada definição original:

```yaml
origem:
destino:
tipo: teste|classe|metodo|fixture|helper|constante|runner
proprietario_unico:
consumidores:
alteracao_permitida: movimentacao_e_imports_mecanicos
```

O mapa deve registrar adicionalmente:

```yaml
_alturas_caixas:
  origem: monolito
  destino: comum.py
  consumidores:
    - _corpo_alturas

_corpo_alturas:
  origem: monolito
  destino: comum.py
  consumidores:
    - composicao_corpo.py
    - matriz_participantes.py

teste_h0037_qapp7_verb_sem_corte_silencioso:
  definicao: conteudo_externo.py
  referencia_adicional:
    modulo: integracao.py
    tipo: alias_privado_nao_coletavel
```

O mapa deve cobrir:

* 72 funções de teste;
* 21 classes;
* 299 métodos de teste;
* 1 fixture;
* 47 helpers;
* `main`;
* constantes e estruturas de módulo inventariadas;
* `sys.dont_write_bytecode`;
* guard de execução direta.

As contagens finais precisam fechar o inventário original.

## 12. Critérios de aceite

Inclua, no mínimo:

1. `tela/teste_renderizador.py` funciona como fachada compatível;
2. `python tela/teste_renderizador.py` preserva ordem, textos, resumo e códigos de saída;
3. `python -m pytest tela/teste_renderizador.py` coleta exatamente 371 casos;
4. a suíte completa coleta e aprova exatamente 970 casos;
5. nenhuma função, classe, método, fixture, helper ou constante é perdida;
6. nenhum teste é coletado duas vezes;
7. classes não são divididas ou renomeadas;
8. decorators, corpos, literais e expectativas permanecem;
9. helpers compartilhados têm proprietário único;
10. não existem ciclos de importação;
11. nenhum módulo proprietário importa a fachada de teste;
12. nenhum `sys.path` novo é criado;
13. produção e testes externos permanecem inalterados;
14. nenhuma decisão funcional é introduzida;
15. defeitos encontrados são apenas registrados e deferidos;
16. a fixture `_fixture_h0041_qa002` possui exatamente uma definição, em `selecao.py`;
17. o nome pytest continua sendo `fixture_h0041_qa002`;
18. a fachada registra a fixture pela importação nominal descrita em 8.2;
19. os testes consumidores da fixture executam pela fachada;
20. os testes consumidores da fixture executam diretamente em `selecao.py`;
21. nenhuma fixture adicional, `conftest.py` ou plugin pytest é criado;
22. compilação e importação de verificação ocorrem inteiramente em memória, sem gravar `.pyc` ou criar `__pycache__` novos;
23. `_alturas_caixas` e `_corpo_alturas` têm propriedade única em `comum.py`;
24. `_corpo_alturas` é consumido somente por composição e matriz;
25. `lancador.py` não consome esses helpers;
26. `integracao.py` possui somente a dependência nominal autorizada para `conteudo_externo.py`;
27. o alias privado não integra `__all__` e não aumenta a coleta;
28. `comum.py` pode importar somente `tela.loader` e `tela.modelo`, além da stdlib;
29. nenhuma outra importação entre proprietários existe.

## 13. Provas estruturais obrigatórias

### 13.1 Inventário AST antes e depois

A implementação deve gerar uma comparação automatizada que normalize somente:

* caminho físico;
* número de linha;
* módulo proprietário.

A prova deve confirmar:

```yaml
funcoes_de_teste: 72
classes_de_teste: 21
metodos_de_teste: 299
testes_coletaveis: 371
fixtures: 1
parametrizacoes: 0
entry_points: 1
guards_de_execucao: 1
```

Também deve confirmar que:

* cada definição aparece uma única vez;
* corpos e decorators permanecem semanticamente equivalentes;
* helpers não foram duplicados;
* o runner preserva sua sequência histórica.

As normalizações mecânicas permitidas incluem:

```yaml
normalizacoes_adicionais:
  - movimentacao conjunta de _alturas_caixas e _corpo_alturas para comum.py
  - substituicao, em test_h0045_ph07_regressao_h0037_console_externo,
    da chamada direta pelo alias privado autorizado
```

A única diferença permitida no corpo do teste consumidor é o identificador
do callee:

```text
teste_h0037_qapp7_verb_sem_corte_silencioso
->
_teste_h0037_qapp7_verb_sem_corte_silencioso
```

Argumentos, ordem, controle de fluxo e demais instruções permanecem
idênticos.

A prova pode ser um script inline executado durante a implementação, mas não deve criar ferramenta permanente sem necessidade.

### 13.2 Coleta pytest

Exigir comparação nominal antes e depois:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q tela/teste_renderizador.py
```

A comparação deve preservar:

* quantidade total de 371;
* classes;
* funções;
* métodos;
* IDs de parametrização;
* ausência de duplicações;
* ausência de colisões.

A mudança do módulo físico deve ser normalizada, mas a identidade semântica do caso deve permanecer.

### 13.3 Propriedade única

Exigir prova automatizada de que cada teste, classe, fixture e helper possui um único proprietário.

Importação pela fachada não pode produzir coleta duplicada. A importação
nominal de `_fixture_h0041_qa002` pela fachada (8.2) não constitui segunda
definição; a prova deve confirmar que a fixture continua definida
exclusivamente em `selecao.py`.

Importação ou alias não constitui definição. O teste H-0037 possui uma
definição; `_alturas_caixas` e `_corpo_alturas` possuem uma definição cada;
nenhuma duplicação é autorizada.

### 13.4 Imports

Exigir prova de:

```yaml
imports:
  proprietario_para_proprietario:
    permitidos:
      - integracao.py -> conteudo_externo.py
        [somente o alias H-0037 nominal]
    demais: proibidos

  comum_para_producao:
    permitidos:
      - tela.loader
      - tela.modelo
    demais: proibidos
```

* importação de todos os módulos;
* ausência de ciclos;
* ausência de `sys.path` novo;
* ausência de caminhos absolutos;
* compatibilidade com execução na raiz;
* módulos proprietários sem dependência da fachada ou do runner.

Importação da fachada por proprietários e importação do runner por
proprietários são proibidas.

As provas de importação e ausência de ciclo devem ser executadas
inteiramente em memória, sem gravação de bytecode nem criação de
`__pycache__`.

## 14. Testes obrigatórios

### 14.1 Compilação e importação

`python -m compileall` é proibido nesta prova: ele grava bytecode em disco
mesmo com `PYTHONDONTWRITEBYTECODE=1`. A compilação é verificada inteiramente
em memória:

```zsh
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
from pathlib import Path

arquivos = [
    Path("tela/teste_renderizador.py"),
    *sorted(Path("tela/testes_renderizador").glob("*.py")),
]

for caminho in arquivos:
    fonte = caminho.read_text(encoding="utf-8")
    compile(fonte, str(caminho), "exec", dont_inherit=True)

print(f"COMPILACAO_EM_MEMORIA: {len(arquivos)}/{len(arquivos)}")
PY
```

Resultado esperado:

```text
COMPILACAO_EM_MEMORIA: 12/12
```

A prova usa os onze arquivos do subpacote e a fachada; não cria `.pyc`,
`__pycache__`, arquivo temporário ou artefato persistente.

A importação real dos módulos é verificada separadamente:

```zsh
PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import importlib

modulos = [
    "tela.testes_renderizador.comum",
    "tela.testes_renderizador.fundamentos",
    "tela.testes_renderizador.barra_menus",
    "tela.testes_renderizador.composicao_corpo",
    "tela.testes_renderizador.matriz_participantes",
    "tela.testes_renderizador.lancador",
    "tela.testes_renderizador.conteudo_externo",
    "tela.testes_renderizador.selecao",
    "tela.testes_renderizador.integracao",
    "tela.testes_renderizador.runner",
    "tela.teste_renderizador",
]

for nome in modulos:
    importlib.import_module(nome)

print(f"IMPORTACAO: {len(modulos)}/{len(modulos)}")
PY
```

Resultado esperado:

```text
IMPORTACAO: 11/11
```

Após compilação, importação e testes, confirmar ausência de resíduos no
novo subpacote:

```zsh
find tela/testes_renderizador \
  \( -type d -name '__pycache__' -o -type f -name '*.pyc' \) \
  -print
```

Resultado esperado: nenhuma saída. Os cinco `.pyc` preexistentes sob
`tela/__pycache__/` permanecem sem alteração e fora do escopo; não há
criação seguida de limpeza — a execução evita resíduos desde a origem.

### 14.2 Coleta da fachada

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q tela/teste_renderizador.py
```

Resultado esperado:

```text
371 testes coletados
```

### 14.3 Execução focal da fachada

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_renderizador.py
```

Resultado esperado:

```text
371 passed
```

### 14.4 Execução dos módulos proprietários

Executar nominalmente:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/testes_renderizador/fundamentos.py \
  tela/testes_renderizador/barra_menus.py \
  tela/testes_renderizador/composicao_corpo.py \
  tela/testes_renderizador/matriz_participantes.py \
  tela/testes_renderizador/lancador.py \
  tela/testes_renderizador/conteudo_externo.py \
  tela/testes_renderizador/selecao.py \
  tela/testes_renderizador/integracao.py
```

Resultado esperado:

```text
371 passed
```

`comum.py` e `runner.py` não devem coletar testes.

Prova focal obrigatória da fixture registrada pela fachada:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_renderizador.py \
  -k 'qah0041_002'
```

O filtro deve coletar pelo menos um caso e todos os casos selecionados devem
passar. Prova complementar da execução direta em `selecao.py`:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/testes_renderizador/selecao.py
```

Resultado esperado:

```text
30 passed
```

### 14.5 Runner direto

```zsh
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
```

Resultado esperado:

* código de saída `0`;
* mesmo cabeçalho;
* mesma sequência;
* mesmos textos;
* mesmo total de verificações do runner histórico;
* nenhum caso H-0044/H-0045 adicionado ao runner direto.

### 14.6 Testes externos preservados

Nenhum arquivo externo será alterado, mas devem ser executados os focos diretamente relacionados:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_navegacao.py \
  tela/teste_paginacao.py \
  tela/teste_resultado_execucao.py \
  demo/teste_demo.py \
  demo/teste_demo_console.py \
  demo/teste_demo_console_modos.py \
  demo/teste_demo_navegacao.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_selecao.py \
  demo/teste_diagnostico.py \
  demo/teste_explorar_barra_de_menus.py
```

O resultado esperado deve ser determinado no baseline antes da alteração e permanecer idêntico depois dela.

### 14.7 Suíte completa

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q
```

Resultado obrigatório:

```text
970 passed
```

Qualquer alteração da quantidade ou falha bloqueia. Não atualizar automaticamente o baseline.

## 15. Demonstração automatizada

Defina uma demonstração sem TTY com sete verificações:

```yaml
demonstracao:
  1: todos os módulos compilam e importam em memória, sem gravar bytecode
  2: fachada coleta 371 casos e registra a fixture por importação nominal de selecao.py
  3: módulos proprietários coletam juntos 371 casos, incluindo os 30 de selecao.py
  4: nenhuma duplicação ou perda
  5: inventário AST preservado
  6: runner direto preservado
  7: suíte completa aprova 970 casos
resultado_esperado: 7_de_7
```

Na demonstração, a verificação de propriedade única deve incluir:

* a cadeia de alturas em `comum.py`;
* uma definição do teste H-0037;
* o alias não coletável em `integracao.py`;
* a ausência de outras dependências entre proprietários.

A implementação deve registrar comandos e resultados no relatório.

Não exigir validação visual ou TTY.

## 16. Relatório de implementação

Exija:

```text
docs/relatorios/IMP-0048-reorganizacao-estrutural-dos-testes-do-renderizador.md
```

Teto normal:

```text
900 palavras
```

O relatório deve registrar apenas:

* arquivos criados e alterados;
* mapa resumido de responsabilidades;
* inventário antes/depois;
* coleta antes/depois;
* runner direto;
* testes focais;
* suíte completa;
* demonstração `7/7`;
* desvios;
* defeitos deferidos;
* bloqueios.

O relatório deve registrar corretamente:

```yaml
fatos:
  - _alturas_caixas e _corpo_alturas pertencem a comum.py
  - _corpo_alturas é consumido por composição e matriz
  - lancador.py não é consumidor
  - integracao.py usa alias privado nominal do teste H-0037
  - comum.py importa tela.loader e tela.modelo
```

Não reproduzir o handoff, código ou listas completas de casos.

## 17. Exceção operacional, reversibilidade e bloqueios

### 17.1 Exceção operacional

Antes de alterar arquivo não autorizado, o implementador deve parar e retornar:

```yaml
status: EXCECAO_OPERACIONAL_NECESSARIA
caminho:
motivo:
escopo:
mudanca_esperada:
impacto_sem_alteracao:
```

Não ampliar autonomamente o escopo.

### 17.2 Reversibilidade

A reversão consiste em:

1. restaurar `tela/teste_renderizador.py` ao conteúdo anterior;
2. remover somente `tela/testes_renderizador/`;
3. remover somente o relatório da implementação;
4. executar novamente coleta, runner direto e suíte completa.

A reversão não altera produção, configuração, backlog, histórico ou o relatório auxiliar.
A reversão não precisa remover caches, porque nenhuma etapa autorizada de
compilação, importação ou teste cria `__pycache__` ou `.pyc` novos.

### 17.3 Bloqueios

Não constituem bloqueio as dependências agora autorizadas: a cadeia de
alturas em `comum.py`, a dependência nominal
`integracao.py → conteudo_externo.py` para o alias H-0037 e os imports de
`tela.loader` e `tela.modelo` por `comum.py`.

Bloquear antes de prosseguir quando houver:

* necessidade de mudar comportamento ou expectativa;
* perda ou duplicação de coleta;
* impossibilidade de preservar o runner direto;
* necessidade de alterar produção;
* necessidade de alterar teste externo;
* divergência entre inventário real e mapa fechado que não possa ser resolvida mecanicamente;
* descoberta de parametrização, fixture ou consumidor não contemplado;
* suíte completa diferente de 970;
* decisão arquitetural nova;
* necessidade de `conftest.py`, plugin pytest, segunda definição, renomeação ou wrapper da fixture;
* geração de `.pyc` ou `__pycache__` novos durante compilação, importação ou testes;
* qualquer consumidor adicional de `_corpo_alturas`;
* qualquer importação adicional entre proprietários;
* qualquer outro import de produção em `comum.py`;
* duplicação de helper ou teste;
* mudança semântica do caso H-0045 PH07;
* alteração das contagens 371/970;
* alteração do runner.

## 18. Relação com os passos anteriores e encerramento do ITEM-0022

Registre:

* H-0046 modularizou a produção do renderizador;
* H-0047 modularizou o loader;
* H-0048 reorganiza apenas os testes;
* nenhum passo anterior é reaberto;
* a implementação do H-0048 completa o terceiro passo técnico, mas não encerra sozinha o item.

O `ITEM-0022` somente poderá ser encerrado depois de:

```yaml
condicoes:
  - H-0048 aprovado
  - implementacao_concluida
  - QA_IMPLEMENTACAO aprovado
  - inventario preservado
  - coleta de 371 casos preservada
  - suite completa com 970 passed
  - demonstracao 7_de_7
  - analise_documental_final concluida
  - commit manual confirmado
```

## 19. Verificação interna do handoff

O documento deve confirmar explicitamente:

* escopo futuro nominal;
* arquivos preservados;
* nenhum arquivo externo autorizado;
* arquitetura baseada em responsabilidades;
* ausência de divisão por tamanho ou linhas;
* propriedade única;
* ausência de perda ou duplicação;
* preservação dos três modos de execução;
* comandos reproduzíveis;
* demonstração objetiva;
* relatório exato;
* reversibilidade;
* ausência de alteração de produção;
* compatibilidade com ADR-0039, H-0046 e H-0047;
* registro da fixture `_fixture_h0041_qa002` por importação nominal exclusiva, sem `conftest.py`, plugin ou segunda definição;
* ausência de bytecode ou cache persistente novo gerado pelas provas de compilação, importação e teste;
* propriedade comum da cadeia de alturas;
* ausência de consumidor em `lancador.py`;
* exceção única `integracao.py → conteudo_externo.py`;
* alias privado não coletável;
* imports restritos de `comum.py`;
* inexistência de outras exceções arquiteturais.
