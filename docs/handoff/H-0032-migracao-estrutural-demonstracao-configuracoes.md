---
name: H-0032-migracao-estrutural-demonstracao-configuracoes
description: Migração estrutural da demonstração, das telas demonstrativas e das configurações gerais conforme ADR-0021, sem criar o produto real
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0032
  data_criacao: 2026-07-15
rastreabilidade:
  adr_principal: docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
  limite_negativo: docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
  relatorios_autoridade:
    - docs/relatorios/RELATORIO_QA_ADR-0021.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
    - docs/relatorios/RELATORIO_QA_ADR-0022.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0022.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0022.md
    - docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
---

# H-0032 - Migracao estrutural da demonstracao e das configuracoes

## 1. Identificacao

Handoff de implementacao: `H-0032`.

Titulo: `Migracao estrutural da demonstracao e das configuracoes`.

Arquivo deste handoff:

```text
docs/handoff/H-0032-migracao-estrutural-demonstracao-configuracoes.md
```

Etapa futura autorizada por este documento: implementacao estrutural da
ADR-0021.

Proxima categoria esperada apos a criacao deste handoff: `QA_HANDOFF`.

## 2. Objetivo

Implementar, em ciclo futuro, a separacao fisica entre motor compartilhado,
aplicacao demonstrativa, telas demonstrativas e configuracoes gerais decidida
pela ADR-0021.

A implementacao futura deve:

1. preservar `tela/` como unico motor compartilhado;
2. mover executaveis e testes demonstrativos para `demo/`;
3. mover telas demonstrativas para `config/telas/demo/`;
4. substituir a identidade demonstrativa inicial `orquestrador` por `demo`;
5. mover configuracoes gerais para `config/layouts/` e `config/elementos/`;
6. atualizar imports, subprocessos, caminhos, comandos e testes afetados;
7. preservar a suite anterior de 1796 verificacoes;
8. impedir aliases, wrappers, copias e fallbacks transitorios;
9. nao criar o Orquestrador real.

## 3. Estado de Origem

Estado fisico observado antes da implementacao:

| Item | Estado |
|---|---|
| `tela/` | existe e mistura motor compartilhado com executaveis e testes demonstrativos |
| `demo/` | nao existe |
| `config/telas/demo/` | nao existe |
| `config/layouts/` | nao existe |
| `config/elementos/` | nao existe |
| `config/telas/orquestrador.json` | existe, possui `"id": "orquestrador"` e representa a demonstracao atual |
| `orquestrador.py` | nao existe |
| `config/estilo.json` | existe e permanece no caminho atual |

Arquivos diretamente em `config/telas/` observados:

```text
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
```

Estado Git observado na criacao deste handoff: stage vazio; workspace com
alteracoes documentais acumuladas das ADRs 0021 e 0022 e relatorios
correspondentes. Esse estado nao impede determinar o escopo porque as
autoridades obrigatorias estao presentes e aprovadas.

## 4. Autoridades

Autoridade principal:

```text
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
```

Limite negativo:

```text
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
```

Relatorios obrigatorios lidos e usados:

```text
docs/relatorios/RELATORIO_QA_ADR-0021.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0021.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0021.md
docs/relatorios/RELATORIO_QA_ADR-0022.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0022.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0022.md
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
```

Contratos ativos materialmente afetados:

```text
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_json_barra_de_menus.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_estilo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_dashboard.md
```

## 5. Decisoes Aplicadas

Decisoes da ADR-0021 aplicadas por este handoff:

| Decisao | Aplicacao futura |
|---|---|
| `tela/` e motor compartilhado | manter loader, modelo, renderizador e seus testes genericos em `tela/` |
| `demo/` e aplicacao demonstrativa | mover para `demo/` apenas entradas, utilitarios e testes demonstrativos |
| `config/telas/demo/` | mover todas as telas demonstrativas para essa raiz |
| identidade demonstrativa | `config/telas/orquestrador.json` vira `config/telas/demo/demo.json` com `"id": "demo"` |
| duas raizes declarativas | demonstracao usa `config/telas/demo/`; produto futuro usa `config/telas/` |
| ausencia de compatibilidade transitoria | nao criar wrappers, aliases, copias nem fallback |
| configuracoes gerais | mover layouts para `config/layouts/` e elementos para `config/elementos/` |
| estilo global | preservar `config/estilo.json` exatamente no caminho atual |

Decisoes da ADR-0022 usadas apenas como limite:

```text
orquestrador.py
config/telas/orquestrador.json real
titulo e descricao da tela real
barra real com Esc, ? e Estilos
tela funcional de estilos
integracao com Pipeline
```

Nenhum desses itens pode ser criado neste ciclo.

## 6. Escopo Positivo

O executor futuro deve:

1. criar os diretorios `demo/`, `config/telas/demo/`, `config/layouts/` e `config/elementos/`;
2. mover nominalmente os arquivos listados nas secoes 10, 11 e 13;
3. alterar somente os arquivos nominalmente autorizados na secao 12;
4. parametrizar a raiz declarativa de tela de modo explicito;
5. atualizar comandos, docstrings operacionais e mensagens de diagnostico em arquivos ativos alterados;
6. atualizar testes existentes e acrescentar testes de raiz/identidade/fallback;
7. criar o relatorio `docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md`;
8. deixar o stage vazio e nao criar commit.

## 7. Escopo Negativo

Nao incluir neste ciclo:

```text
orquestrador.py
config/telas/orquestrador.json como tela real nova
titulo ou descricao da tela real
barra real com Esc, ? ou Estilos
acao, tecla ou destino de Estilos
tela funcional de estilos
integracao com Pipeline
destino_minimo: correcao de preenchimento
grupo_minimo: correcao de preenchimento
alteracao funcional de layout
alteracao de schema
novos tipos de elemento
mudanca de bordas
mudanca de envelopes de chips
persistencia de estilo
```

`destino_minimo.json` e `grupo_minimo.json` devem ser apenas movidos.

## 8. Estrutura Atual

```text
config/
  barra_de_menus.json
  cabecalho.json
  estilo.json
  lancador.json
  layout_console.json
  layout_dado.json
  layout_menu.json
  telas/
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
    orquestrador.json
    stub_b.json
tela/
  __init__.py
  demo.py
  diagnostico.py
  explorar_barra_de_menus.py
  loader.py
  modelo.py
  renderizador.py
  teste_demo.py
  teste_diagnostico.py
  teste_explorar_barra_de_menus.py
  teste_loader.py
  teste_modelo.py
  teste_renderizador.py
```

## 9. Estrutura Final

```text
config/
  estilo.json
  elementos/
    barra_de_menus.json
    cabecalho.json
    lancador.json
  layouts/
    layout_console.json
    layout_dado.json
    layout_menu.json
  telas/
    demo/
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
demo/
  demo.py
  diagnostico.py
  explorar_barra_de_menus.py
  teste_demo.py
  teste_diagnostico.py
  teste_explorar_barra_de_menus.py
tela/
  __init__.py
  loader.py
  modelo.py
  renderizador.py
  teste_loader.py
  teste_modelo.py
  teste_renderizador.py
```

`config/telas/` fica reservado ao produto real, mas este ciclo nao cria arquivo
diretamente nele.

## 10. Arquivos Movidos

| Origem | Destino |
|---|---|
| `tela/demo.py` | `demo/demo.py` |
| `tela/diagnostico.py` | `demo/diagnostico.py` |
| `tela/explorar_barra_de_menus.py` | `demo/explorar_barra_de_menus.py` |
| `tela/teste_demo.py` | `demo/teste_demo.py` |
| `tela/teste_diagnostico.py` | `demo/teste_diagnostico.py` |
| `tela/teste_explorar_barra_de_menus.py` | `demo/teste_explorar_barra_de_menus.py` |
| `config/telas/destino_minimo.json` | `config/telas/demo/destino_minimo.json` |
| `config/telas/grupo_minimo.json` | `config/telas/demo/grupo_minimo.json` |
| `config/telas/h0029_dashboard_fracao.json` | `config/telas/demo/h0029_dashboard_fracao.json` |
| `config/telas/h0029_dashboard_igual.json` | `config/telas/demo/h0029_dashboard_igual.json` |
| `config/telas/h0029_dashboard_percentual.json` | `config/telas/demo/h0029_dashboard_percentual.json` |
| `config/telas/h0029_grupo_fracao.json` | `config/telas/demo/h0029_grupo_fracao.json` |
| `config/telas/h0029_grupo_igual.json` | `config/telas/demo/h0029_grupo_igual.json` |
| `config/telas/h0029_grupo_pai_distribuido.json` | `config/telas/demo/h0029_grupo_pai_distribuido.json` |
| `config/telas/h0029_grupo_percentual.json` | `config/telas/demo/h0029_grupo_percentual.json` |
| `config/telas/h0030_console_unico.json` | `config/telas/demo/h0030_console_unico.json` |
| `config/telas/h0030_dashboard_unico.json` | `config/telas/demo/h0030_dashboard_unico.json` |
| `config/telas/h0030_matriz_2x2.json` | `config/telas/demo/h0030_matriz_2x2.json` |
| `config/telas/h0030_matriz_2x4.json` | `config/telas/demo/h0030_matriz_2x4.json` |
| `config/telas/h0030_matriz_3x2.json` | `config/telas/demo/h0030_matriz_3x2.json` |
| `config/telas/stub_b.json` | `config/telas/demo/stub_b.json` |
| `config/layout_console.json` | `config/layouts/layout_console.json` |
| `config/layout_dado.json` | `config/layouts/layout_dado.json` |
| `config/layout_menu.json` | `config/layouts/layout_menu.json` |
| `config/cabecalho.json` | `config/elementos/cabecalho.json` |
| `config/barra_de_menus.json` | `config/elementos/barra_de_menus.json` |
| `config/lancador.json` | `config/elementos/lancador.json` |

## 11. Arquivos Renomeados

| Origem | Destino | Alteracao interna autorizada |
|---|---|---|
| `config/telas/orquestrador.json` | `config/telas/demo/demo.json` | alterar somente o campo `"id": "orquestrador"` para `"id": "demo"`; todos os demais campos e valores devem ser preservados sem alteracao funcional ou textual |

Nao criar alias entre `orquestrador` e `demo`.

Autorizacao de conteudo fechada:

```yaml
arquivo: config/telas/demo/demo.json
origem: config/telas/orquestrador.json
alteracao_de_conteudo_autorizada:
  campo: id
  valor_anterior: orquestrador
  valor_novo: demo
demais_campos: PRESERVAR
campos_proibidos_de_alterar:
  - schema
  - cabecalho
  - titulo
  - descricao
  - corpo
  - textos
  - chips
  - teclas
  - acoes
  - destinos
  - layouts
  - dados_demonstrativos
  - qualquer_outro_campo
```

Se qualquer outro campo precisar ser alterado para a implementacao passar, o
executor deve parar e solicitar autorizacao explicita do usuario antes da
alteracao.

## 12. Arquivos Modificados

Arquivos de motor compartilhado:

| Arquivo | Mudanca autorizada |
|---|---|
| `tela/loader.py` | aceitar raiz declarativa explicita; preservar validacao `id`/basename; remover dependencia rigida de `config/telas/<id>.json`; nao adicionar fallback |
| `tela/teste_loader.py` | atualizar fixtures, helpers e testes para produto em `config/telas/` e demo em `config/telas/demo/`; acrescentar testes obrigatorios de raiz/ausencia de fallback |
| `tela/teste_modelo.py` | atualizar chamadas que carregam telas demonstrativas para a raiz demo explicita |
| `tela/teste_renderizador.py` | atualizar chamadas que carregam telas demonstrativas para a raiz demo explicita; preservar snapshots exceto identidade demonstrativa autorizada |

Modulos de motor compartilhado preservados sem autorizacao de escrita (ver secao 14):

```yaml
arquivo: tela/modelo.py
tratamento: PRESERVADO
alteracao_autorizada: nao
justificativa: nenhuma dependencia de caminho ou identidade demonstrativa comprovada

arquivo: tela/renderizador.py
tratamento: PRESERVADO
alteracao_autorizada: nao
justificativa: nenhuma dependencia de caminho ou identidade demonstrativa comprovada
```

A leitura e a execucao dos testes em `tela/teste_modelo.py` e
`tela/teste_renderizador.py` permanecem permitidas.

Regra de excecao para `tela/modelo.py` e `tela/renderizador.py`: se durante a
implementacao surgir necessidade inesperada de alterar qualquer um desses
arquivos, o executor deve:

1. parar antes da alteracao;
2. informar o arquivo;
3. apresentar a evidencia;
4. justificar a necessidade;
5. limitar o escopo;
6. solicitar autorizacao explicita ao usuario;
7. registrar a autorizacao no relatorio de implementacao.

Nao tratar essa excecao como autorizacao antecipada.

Arquivos demonstrativos movidos para `demo/`:

| Arquivo final | Mudanca autorizada |
|---|---|
| `demo/demo.py` | importar motor de `tela.*`; iniciar por `demo`; selecionar explicitamente `config/telas/demo/`; atualizar docstrings e bootstrap para novo caminho |
| `demo/diagnostico.py` | importar motor de `tela.*`; padrao `demo`; selecionar explicitamente `config/telas/demo/`; atualizar docstrings e modo executavel |
| `demo/explorar_barra_de_menus.py` | manter uso do renderer compartilhado; atualizar docstrings, `_BASE` e caminho de subprocess nos testes |
| `demo/teste_demo.py` | atualizar imports, subprocessos, caminhos JSON, estado inicial, snapshots e mensagens de `orquestrador` demonstrativo para `demo` |
| `demo/teste_diagnostico.py` | atualizar imports, subprocessos, expected output e mensagens para `demo/diagnostico.py` e identidade `demo` |
| `demo/teste_explorar_barra_de_menus.py` | atualizar `_SCRIPT` para `demo/explorar_barra_de_menus.py` e docstrings operacionais |

Documentos ativos que podem ser alterados somente para comandos operacionais
ativos ou indices vivos afetados pela mudanca fisica:

```text
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_lancador.md
```

Se a busca comprovar que esses documentos ja estao normativamente corretos e
nao contem comando operacional ativo quebrado, nao altera-los.

## 13. Diretorios Criados

```text
demo/
config/telas/demo/
config/layouts/
config/elementos/
```

## 14. Arquivos Preservados

Devem permanecer em `tela/`:

```text
tela/__init__.py
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Registro explícito de preservacao sem autorizacao de escrita:

```yaml
arquivo: tela/modelo.py
tratamento: PRESERVADO
alteracao_autorizada: nao
justificativa: nenhuma dependencia de caminho ou identidade demonstrativa comprovada

arquivo: tela/renderizador.py
tratamento: PRESERVADO
alteracao_autorizada: nao
justificativa: nenhuma dependencia de caminho ou identidade demonstrativa comprovada
```

Deve permanecer exatamente no caminho atual:

```text
config/estilo.json
```

Historicos e evidencias devem permanecer preservados salvo referencia
operacional ativa comprovada:

```text
docs/handoff/H-0001-loader-validador-tela-json.md
docs/handoff/H-0002-modelo-interno-tela.md
docs/handoff/H-0003-renderizador-textual-estatico.md
docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
docs/handoff/H-0006-tela-minima-borda-fixa.md
docs/handoff/H-0007-alternancia-bordas-memoria.md
docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md
docs/handoff/H-0010-lancador-visual-inerte.md
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md
docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md
docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md
docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
docs/handoff/H-0023-redimensionamento-reativo-tui.md
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md
docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
docs/handoff/H-0030-catalogo-telas-utilizaveis.md
docs/handoff/H-0031-migracao-repositorio-orquestrador-raiz-independente.md
```

Relatorios historicos `docs/relatorios/IMP-*`, `docs/relatorios/RELATORIO_QA_H-*`,
`docs/relatorios/RELATORIO_AUDITORIA_*` e evidencias historicas nao devem ser
alterados apenas por conterem caminhos antigos.

Arquivos proibidos:

```text
demo/__init__.py
orquestrador.py
config/telas/orquestrador.json
config/estilos/
config/telas/demo/orquestrador.json
tela/demo.py
tela/diagnostico.py
tela/explorar_barra_de_menus.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
```

Os seis ultimos caminhos sao proibidos como arquivos remanescentes apos a
migracao. Eles devem deixar de existir nesses caminhos antigos.

## 15. Politica das Raizes

Raizes declarativas finais:

```text
demonstracao: config/telas/demo/
produto futuro: config/telas/
```

Regra de implementacao:

- a demonstracao deve selecionar explicitamente `config/telas/demo/`;
- o motor compartilhado deve aceitar a raiz declarativa por parametro ou
  configuracao explicita da chamada;
- a raiz padrao historica nao pode ser usada para buscar telas da demonstracao;
- `config/telas/` fica preservado para produto futuro;
- `config/telas/demo/` nao e fallback de `config/telas/`;
- `config/telas/` nao e fallback de `config/telas/demo/`.

Sao proibidos:

```text
busca automatica em ambas as raizes
tentativa na raiz real seguida de fallback para demonstracao
tentativa na demonstracao seguida de fallback para raiz real
alias de id
copia do mesmo JSON nas duas raizes
resolucao baseada apenas em coincidencia de nome
```

## 16. Mudancas Necessarias no Loader

Arquivo: `tela/loader.py`.

Simbolos atuais afetados:

| Simbolo | Estado atual | Mudanca obrigatoria |
|---|---|---|
| `_ID_TELA_RAIZ` | fixa `"orquestrador"` como raiz historica | remover uso como regra especial para a demonstracao; se permanecer, deve ser restrito a produto futuro e nao afetar `demo` |
| `_caminho_padrao_base()` | calcula raiz operacional pelo pai de `tela/` | pode permanecer como raiz do repositorio, nao como raiz declarativa |
| `carregar_tela(caminho_base, id_tela)` | monta `config/telas/<id>.json` internamente | aceitar raiz declarativa explicita, por exemplo `raiz_declarativa`, `diretorio_telas` ou objeto equivalente |
| `TelaIdNaoCoincideComArquivo` | valida `id` contra basename | preservar integralmente nas duas raizes |
| `TelaIdIncorreto` | valida caso especial de `orquestrador` | revisar para nao impedir `demo`; nao criar alias |

Implementacao esperada:

1. `carregar_tela` deve conseguir carregar `demo` em `config/telas/demo/demo.json`;
2. `carregar_tela` deve continuar conseguindo carregar produto futuro em `config/telas/<id>.json` quando a raiz `config/telas/` for explicitamente selecionada;
3. mensagens de erro devem citar o caminho relativo efetivamente tentado;
4. ausencia de arquivo em uma raiz nao deve disparar tentativa na outra raiz;
5. os testes devem cobrir erro deterministico quando o id existe apenas na outra raiz.

Se o executor concluir que nao e possivel especificar a mudanca sem nova
decisao arquitetural, deve parar com:

```text
ARCHITECTURE_REVIEW_REQUIRED
```

## 17. Mudancas nos Executaveis

Arquivos finais e chamadas:

| Arquivo | Mudancas obrigatorias |
|---|---|
| `demo/demo.py` | `criar_estado_inicial()` deve usar `tela_atual: "demo"`; `_carregar_modelo_por_id()` deve chamar o loader com raiz `config/telas/demo/`; subprocessos e docstrings devem mencionar `python demo/demo.py` |
| `demo/diagnostico.py` | `gerar_diagnostico_tela()` deve ter padrao `"demo"`; chamada ao loader deve selecionar `config/telas/demo/`; modo executavel deve ser `python demo/diagnostico.py` |
| `demo/explorar_barra_de_menus.py` | manter cenarios sinteticos; atualizar docstring para `python demo/explorar_barra_de_menus.py`; manter import do renderer em `tela.renderizador` |

Imports:

```text
from tela.loader import carregar_tela
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import renderizar_tela, RenderizadorErro
```

Esses imports devem continuar apontando para o motor compartilhado em `tela/`.
Nao copiar loader, modelo ou renderizador para `demo/`.

Politica de `demo/__init__.py`: nao criar. A inspecao do codigo atual mostra
que todos os seis scripts possuem bootstrap explicito para inserir a raiz do
repositorio em `sys.path`. Nenhum script depende exclusivamente de
`CWD = raiz_do_repositorio` para importar `tela.*`.

Scripts executaveis (`demo.py`, `diagnostico.py`): calculam a raiz via
manipulacao de string em `__file__`, removendo 2 componentes finais (`[:-2]`).
O resultado e identico em `tela/` ou `demo/` porque a profundidade e a mesma.

Scripts de teste e explorador (`explorar_barra_de_menus.py`, `teste_demo.py`,
`teste_diagnostico.py`, `teste_explorar_barra_de_menus.py`): calculam a raiz
via `Path(__file__).resolve().parent.parent`. Apos a movimentacao para `demo/`,
`parent.parent` continua apontando para a raiz do repositorio.

Todos os seis comandos de teste devem ser executados com o diretorio atual
igual a raiz do repositorio.

Importacao via namespace package e suficiente se necessario. `demo/__init__.py`:
necessidade `NAO_CONFIRMADA`; criacao proibida sem autorizacao explicita. Se o
executor provar que `demo/__init__.py` e estritamente indispensavel, deve parar
antes de cria-lo e pedir autorizacao explicita ao usuario.

Se a inspecao demonstrar que os comandos nao funcionam sem novo bootstrap ou
sem `demo/__init__.py`, o executor deve parar e solicitar autorizacao explicita
antes da criacao ou da mudanca adicional.

Mecanismo de importacao por arquivo (estado atual, antes da movimentacao):

```yaml
imports_apos_movimentacao:
  demo/demo.py:
    mecanismo_atual: bootstrap via string — _raiz_scripts remove 2 componentes finais de __file__; sys.path.insert(0, _raiz_scripts)
    mecanismo_preservado: em demo/demo.py a profundidade e identica a tela/demo.py; raiz do repositorio preservada
    depende_de_cwd_raiz: nao
  demo/diagnostico.py:
    mecanismo_atual: bootstrap via string — mesmo padrao de demo.py (linha 44 de tela/diagnostico.py); sys.path.insert(0, _raiz_scripts)
    mecanismo_preservado: em demo/diagnostico.py a profundidade e identica a tela/diagnostico.py; raiz do repositorio preservada
    depende_de_cwd_raiz: nao
  demo/explorar_barra_de_menus.py:
    mecanismo_atual: bootstrap via pathlib — _BASE = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(_BASE))
    mecanismo_preservado: em demo/explorar_barra_de_menus.py, parent.parent preserva a raiz do repositorio
    depende_de_cwd_raiz: nao
  demo/teste_demo.py:
    bootstrap_explicito: sim — _BASE_PADRAO = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(_BASE_PADRAO))
    convencao_de_execucao: execucao da raiz recomendada; bootstrap torna CWD opcional
  demo/teste_diagnostico.py:
    bootstrap_explicito: sim — _BASE_PADRAO = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(_BASE_PADRAO))
    convencao_de_execucao: execucao da raiz recomendada; bootstrap torna CWD opcional
  demo/teste_explorar_barra_de_menus.py:
    bootstrap_explicito: sim — _BASE = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(_BASE))
    convencao_de_execucao: execucao da raiz recomendada; bootstrap torna CWD opcional
```

## 18. Mudancas nos Testes

Testes que permanecem em `tela/`:

```text
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Testes que devem mover para `demo/`:

```text
demo/teste_demo.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
```

Atualizacoes obrigatorias nos testes:

| Arquivo | Atualizacoes |
|---|---|
| `tela/teste_loader.py` | helpers devem criar telas temporarias sob raiz declarativa explicita; testes reais da demonstracao devem usar `config/telas/demo/`; adicionar teste de ausencia de fallback entre raizes; preservar teste de coincidencia `id`/basename |
| `tela/teste_modelo.py` | chamadas a telas demonstrativas devem selecionar raiz demo; referencias de identidade inicial demonstrativa passam para `demo` |
| `tela/teste_renderizador.py` | chamadas a telas demonstrativas devem selecionar raiz demo; snapshots que exibem titulo/identidade da demonstracao devem ser atualizados somente quando decorrentes da mudanca `demo` |
| `demo/teste_demo.py` | imports devem apontar para `demo.demo`; subprocessos devem chamar `demo/demo.py`; caminhos de JSON devem apontar para `config/telas/demo/demo.json`; estado inicial e pilha devem usar `demo` |
| `demo/teste_diagnostico.py` | imports devem apontar para `demo.diagnostico`; subprocessos devem chamar `demo/diagnostico.py`; expected output deve refletir identidade demonstrativa `demo` |
| `demo/teste_explorar_barra_de_menus.py` | `_SCRIPT` deve apontar para `demo/explorar_barra_de_menus.py`; imports do renderer permanecem em `tela.renderizador` |

Subprocessos ativos a atualizar nominalmente:

```text
[sys.executable, "tela/demo.py"] -> [sys.executable, "demo/demo.py"]
[sys.executable, "tela/diagnostico.py"] -> [sys.executable, "demo/diagnostico.py"]
_BASE / "tela" / "explorar_barra_de_menus.py" -> _BASE / "demo" / "explorar_barra_de_menus.py"
```

Nao preservar scripts nos caminhos antigos.

## 19. Mudancas nas Configuracoes

Telas demonstrativas:

- mover todos os JSONs listados nas secoes 10 e 11 para `config/telas/demo/`;
- manter nomes e IDs internos inalterados para todos, exceto a atual tela
  `orquestrador`;
- renomear `config/telas/orquestrador.json` para `config/telas/demo/demo.json`;
- alterar o campo interno dessa tela para `"id": "demo"`;
- nao alterar `destino_minimo.json` e `grupo_minimo.json` para corrigir
  preenchimento;
- nao criar `config/telas/demo/orquestrador.json`.

Configuracoes gerais:

| Origem | Destino |
|---|---|
| `config/layout_console.json` | `config/layouts/layout_console.json` |
| `config/layout_dado.json` | `config/layouts/layout_dado.json` |
| `config/layout_menu.json` | `config/layouts/layout_menu.json` |
| `config/cabecalho.json` | `config/elementos/cabecalho.json` |
| `config/barra_de_menus.json` | `config/elementos/barra_de_menus.json` |
| `config/lancador.json` | `config/elementos/lancador.json` |

Essa movimentacao nao altera conteudo, schema, semantica, status ativo,
transicional ou obsoleto, nem valores de configuracao.

`config/estilo.json` permanece intacto.

## 20. Busca de Referencias

Antes de implementar, executar da raiz:

```bash
rg -n \
  'tela/demo\.py|tela/diagnostico\.py|tela/explorar_barra_de_menus\.py|tela/teste_demo\.py|tela/teste_diagnostico\.py|tela/teste_explorar_barra_de_menus\.py|config/telas/orquestrador\.json|config/telas/|config/layout_console\.json|config/layout_dado\.json|config/layout_menu\.json|config/cabecalho\.json|config/barra_de_menus\.json|config/lancador\.json'
```

Classificacao obrigatoria das ocorrencias:

| Classe | Tratamento |
|---|---|
| codigo ativo | alterar se estiver nos arquivos nominalmente autorizados |
| teste ativo | alterar se estiver nos arquivos nominalmente autorizados |
| comando operacional ativo | alterar se for comando vivo de execucao da suite ou da demonstracao |
| documento normativo ativo | alterar somente se a aplicacao documental ainda nao estiver correta ou se houver comando ativo quebrado |
| historico | preservar |
| relatorio | preservar, exceto o relatorio novo `IMP-0032` |
| handoff anterior | preservar |
| sem impacto | preservar |

Arquivos ativos ja identificados para alteracao:

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
config/telas/demo/demo.json
```

Arquivos de motor compartilhado preservados sem autorizacao de escrita (ver secoes 12 e 14):

```text
tela/modelo.py
tela/renderizador.py
```

A busca pode encontrar ocorrencias nesses arquivos; isso nao concede
autorizacao de escrita. Qualquer alteracao necessaria exige a excecao focal
prevista na secao 12.

Arquivos ativos a alterar somente se a busca comprovar referencia operacional
ativa restante:

```text
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_cabecalho.md
docs/contratos/contrato_json_cabecalho.md
docs/contratos/contrato_lancador.md
```

Nao fazer substituicao textual global por substring.

## 21. Referencias Historicas Preservadas

Preservar referencias antigas em:

```text
docs/handoff/H-0001-loader-validador-tela-json.md
docs/handoff/H-0002-modelo-interno-tela.md
docs/handoff/H-0003-renderizador-textual-estatico.md
docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
docs/handoff/H-0006-tela-minima-borda-fixa.md
docs/handoff/H-0007-alternancia-bordas-memoria.md
docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md
docs/handoff/H-0010-lancador-visual-inerte.md
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md
docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md
docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md
docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
docs/handoff/H-0023-redimensionamento-reativo-tui.md
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md
docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
docs/handoff/H-0030-catalogo-telas-utilizaveis.md
docs/handoff/H-0031-migracao-repositorio-orquestrador-raiz-independente.md
docs/relatorios/IMP-0001-loader-validador-tela-json.md
docs/relatorios/IMP-0002-modelo-interno-tela.md
docs/relatorios/IMP-0003-renderizador-textual-estatico.md
docs/relatorios/IMP-0004-diagnostico-executavel-tela-raiz.md
docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md
docs/relatorios/IMP-0006-tela-minima-borda-fixa.md
docs/relatorios/IMP-0007-alternancia-bordas-memoria.md
docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md
docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md
docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md
docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md
docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
docs/relatorios/IMP-0018-cobertura-executavel-distribuicao-barra-de-menus.md
docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md
docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md
docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md
```

## 22. Suite Obrigatoria

Linha de base anterior: `1796/1796`.

Linha de base individual por script (estado pre-migracao):

```yaml
suite_baseline:
  tela/teste_loader.py: 244/244
  tela/teste_modelo.py: 148/148
  tela/teste_renderizador.py: 980/980
  tela/teste_demo.py: 358/358
  tela/teste_diagnostico.py: 28/28
  tela/teste_explorar_barra_de_menus.py: 38/38
  total: 1796/1796
```

Comandos obrigatorios, executados da raiz apos a migracao:

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python demo/teste_demo.py
python demo/teste_diagnostico.py
python demo/teste_explorar_barra_de_menus.py
```

A suite final deve preservar todos os 1796 testes anteriores. O total pode
superar 1796 por novos testes obrigatorios. Qualquer aumento deve ser
explicado pela adicao nominal de testes.

Nenhum script pode terminar com quantidade inferior a sua linha de base:

```yaml
tela/teste_loader.py: 244
tela/teste_modelo.py: 148
tela/teste_renderizador.py: 980
demo/teste_demo.py: 358
demo/teste_diagnostico.py: 28
demo/teste_explorar_barra_de_menus.py: 38
```

O total final deve ser igual ou superior a 1796.

Qualquer reducao individual ou total e bloqueante, mesmo que outro script
tenha aumentado.

Novos testes obrigatorios:

1. carregamento da demonstracao com raiz `config/telas/demo/`;
2. carregamento do produto futuro com raiz `config/telas/` usando fixture
   temporaria, sem criar tela real no repositorio;
3. ausencia de fallback entre as duas raizes;
4. coincidencia entre nome do arquivo e `id` em `config/telas/demo/`;
5. identidade inicial demonstrativa `demo`;
6. subprocessos chamando `demo/...`;
7. ausencia de referencias ativas aos scripts antigos;
8. `config/estilo.json` intacto;
9. ausencia de `config/telas/demo/orquestrador.json`;
10. ausencia de `orquestrador.py`.

Uma reducao do total anterior sem justificativa e bloqueante.

Executar tambem:

```bash
git diff --check
```

## 23. Demonstracao Operacional

A implementacao futura deve executar o ponto de entrada demonstrativo:

```bash
python demo/diagnostico.py
```

ou, se `demo/diagnostico.py` nao emitir evidencia suficiente, deve usar teste
dedicado da suite que comprove semanticamente:

- script executado sob `demo/`;
- identidade carregada `demo`;
- raiz declarativa `config/telas/demo/`;
- ausencia de carregamento por alias `orquestrador`;
- funcionamento do motor compartilhado em `tela/`;
- ausencia de fallback para `config/telas/`.

Codigo de saida zero isolado e insuficiente. A prova deve ser textual e
reproduzivel no relatorio de implementacao.

## 24. Validacao Manual

Nao ha validacao visual/TTY obrigatoria para aceitar este ciclo se os testes e
o diagnostico textual comprovarem identidade, raiz e ausencia de fallback.

Se o executor concluir que a interface TTY real precisa ser validada para
alguma regressao material, deve registrar:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

O executor nao deve simular aprovacao visual.

## 25. Relatorio de Implementacao

Criar:

```text
docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md
```

O relatorio deve registrar:

- estado Git inicial;
- arquivos movidos;
- arquivos renomeados;
- arquivos alterados;
- diretorios criados;
- mecanismo explicito de selecao da raiz;
- referencias atualizadas;
- referencias historicas preservadas;
- comandos executados;
- testes por script com contagem individual (contagem_baseline e contagem_final para cada script; qualquer reducao individual e bloqueante);
- total da suite;
- evidencia da identidade `demo`;
- evidencia da raiz demonstrativa;
- ausencia de alias, wrapper e fallback;
- estado Git final;
- bloqueios;
- arquivos fora do escopo observados;
- qualquer autorizacao focal do usuario.

## 26. Criterios de Aceite

1. `tela/` permanece como motor unico.
2. `demo/` contem somente os tres executaveis e tres testes demonstrativos previstos.
3. Os scripts antigos nao permanecem em `tela/`.
4. Todas as telas demonstrativas estao em `config/telas/demo/`.
5. `config/telas/demo/demo.json` possui `"id": "demo"`.
6. Nenhuma tela demonstrativa permanece diretamente em `config/telas/`.
7. As configuracoes gerais estao em `config/layouts/` e `config/elementos/`.
8. `config/estilo.json` permanece intacto.
9. A raiz demonstrativa e selecionada explicitamente.
10. Nao ha alias, wrapper ou fallback.
11. Todas as referencias operacionais afetadas foram atualizadas somente nos arquivos nominalmente autorizados na secao 12 (escopo de escrita). As buscas finais nao apresentam referencias operacionais residuais aos caminhos antigos nesses arquivos. Qualquer arquivo adicional encontrado nao esta automaticamente autorizado e exige a excecao focal prevista na secao 28.
12. A suite anterior de 1796 verificacoes foi preservada e cada script final manteve no minimo sua linha de base individual: `tela/teste_loader.py` >= 244, `tela/teste_modelo.py` >= 148, `tela/teste_renderizador.py` >= 980, `demo/teste_demo.py` >= 358, `demo/teste_diagnostico.py` >= 28, `demo/teste_explorar_barra_de_menus.py` >= 38. Reducao individual e bloqueante mesmo que outro script tenha aumentado.
13. Os novos testes de raiz e identidade passam.
14. A demonstracao operacional comprova `demo`.
15. Nenhum artefato do produto real foi criado.
16. Nenhum problema de preenchimento foi corrigido incidentalmente.
17. Stage permanece vazio.
18. Nenhum commit foi criado.

Verificacao do criterio 11 — busca de caminhos residuais (executar da raiz apos a migracao):

```bash
rg -n \
  'tela/demo\.py|tela/diagnostico\.py|tela/explorar_barra_de_menus\.py|tela/teste_demo\.py|tela/teste_diagnostico\.py|tela/teste_explorar_barra_de_menus\.py|config/telas/orquestrador\.json|config/layout_console\.json|config/layout_dado\.json|config/layout_menu\.json|config/cabecalho\.json|config/barra_de_menus\.json|config/lancador\.json'
```

Cada ocorrencia encontrada deve ser classificada como:

- atualizada em arquivo nominal;
- historica e preservada;
- relatorio ou handoff fechado;
- fora do escopo;
- bloqueio por arquivo adicional necessario.

A busca nao concede autorizacao de escrita.

## 27. Condicoes de Bloqueio

Parar com `BLOCKED_USER_DECISION` quando:

- `demo/__init__.py` for indispensavel e nao houver autorizacao explicita;
- a migracao exigir alterar schema;
- um arquivo ativo necessario estiver fora do escopo nominal deste handoff;
- for necessario incluir a tela real para manter a suite;
- a implementacao estrutural exigir corrigir `destino_minimo` ou `grupo_minimo`;
- qualquer lacuna exigir escolher comportamento funcional.

Parar com `BLOCKED_DOCUMENTATION` quando:

- uma autoridade obrigatoria estiver ausente;
- houver contradicao ativa entre documentos;
- o estado Git impedir determinar o escopo;
- o ID H-0032 ja estiver ocupado em outro arquivo.

Parar com `ARCHITECTURE_REVIEW_REQUIRED` quando:

- a selecao explicita da raiz nao puder ser implementada como parametrizacao
  do loader/chamadas sem decisao arquitetural nova.

## 28. Regra de Arquivo Adicional

Se um arquivo adicional for comprovadamente necessario durante a implementacao
e nao estiver nominalmente autorizado, o executor deve:

1. parar;
2. informar o arquivo;
3. explicar a necessidade;
4. descrever o escopo exato;
5. pedir autorizacao explicita ao usuario.

Nao e necessario patch retroativo deste handoff quando a excecao for autorizada
pelo usuario, mas o relatorio de implementacao deve registrar a autorizacao.

## 29. Proibicoes Git

Durante a implementacao:

- nao executar `git add`;
- nao executar `git stash`, `git stash push`, `git stash pop`, `git stash apply`, `git stash drop` nem `git stash clear`;
- nao executar `git commit`;
- nao criar commit;
- nao deixar stage com arquivos;
- nao reverter alteracoes do usuario;
- nao limpar historicos;
- nao usar comandos destrutivos para substituir movimentacoes nominais.

O relatorio final deve comprovar stage vazio.

## 30. Avaliacao de Coesao

Classificacao:

```text
HANDOFF_COESO
```

Justificativa:

- todas as mudancas dependem da mesma politica de caminhos da ADR-0021;
- scripts, testes, telas demonstrativas e configuracoes gerais precisam ser
  atualizados no mesmo ciclo para evitar wrappers e fallbacks proibidos;
- os testes podem ser executados como uma unica suite;
- nao ha segunda capacidade funcional independente;
- o produto real da ADR-0022 fica explicitamente fora do escopo;
- o relatorio de implementacao pode manter rastreabilidade nominal completa.

## 31. Saida Esperada do Executor

Ao concluir a implementacao futura, o executor deve responder:

```text
etapa: IMPLEMENTAR_HANDOFF
handoff: docs/handoff/H-0032-migracao-estrutural-demonstracao-configuracoes.md
resultado:
relatorio: docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md
arquivos_movidos:
arquivos_renomeados:
arquivos_modificados:
diretorios_criados:
arquivos_criados:
suite:
  tela/teste_loader.py:
    contagem_baseline: 244
    contagem_final:
    novos_testes:
    falhas:
    codigo_saida:
  tela/teste_modelo.py:
    contagem_baseline: 148
    contagem_final:
    novos_testes:
    falhas:
    codigo_saida:
  tela/teste_renderizador.py:
    contagem_baseline: 980
    contagem_final:
    novos_testes:
    falhas:
    codigo_saida:
  demo/teste_demo.py:
    contagem_baseline: 358
    contagem_final:
    novos_testes:
    falhas:
    codigo_saida:
  demo/teste_diagnostico.py:
    contagem_baseline: 28
    contagem_final:
    novos_testes:
    falhas:
    codigo_saida:
  demo/teste_explorar_barra_de_menus.py:
    contagem_baseline: 38
    contagem_final:
    novos_testes:
    falhas:
    codigo_saida:
  total_baseline: 1796
  total_final:
validacao_operacional:
validacao_manual:
bloqueios:
stage:
commit:
proxima_categoria: QA_IMPLEMENTACAO
```

Usar `proxima_categoria: QA_IMPLEMENTACAO` somente se a implementacao terminar
completa, sem bloqueio, com stage vazio e sem commit.

## 32. Controle de Alteracoes

```text
2026-07-15: Criacao do handoff H-0032 para a migracao estrutural da ADR-0021,
usando a ADR-0022 apenas como limite negativo e preservando a tela real fora
do escopo.
2026-07-15: Patch PATCH_HANDOFF (2) — corrige B-001 residual: expande criterio
12 da secao 26 para declarar minimos individuais por script e a regra de que
reducao individual e bloqueante mesmo com aumento em outro script.
2026-07-15: Patch PATCH_HANDOFF — corrige M-001 (remove tela/modelo.py e
tela/renderizador.py da lista de modificacao; registra como PRESERVADOS com
justificativa e regra de excecao focal), M-002 (fecha autorizacao de conteudo
de config/telas/demo/demo.json ao campo id exclusivamente; lista campos
proibidos), B-001 (adiciona baseline individual por script; exige minimo por
script; expande suite na saida do executor), B-002 (proibe git stash e
variantes), B-003 (atualiza criterio 11 com referencia nominal a secao 12;
adiciona rg de verificacao e classificacao de ocorrencias), B-004 (corrige
descricao de mecanismo de bootstrap por arquivo; adiciona tabela
imports_apos_movimentacao).
```
